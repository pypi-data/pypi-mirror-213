import abc
from typing import List, AsyncGenerator, Union, Optional, TypedDict

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import nullslast

from kaiju_tools.exceptions import ValidationError, NotFound, Conflict, InternalError, MethodNotAllowed
from kaiju_tools.services import Service
from kaiju_db.transport import DatabaseService

__all__ = ['SQLService', 'ErrorCodes']


class ErrorCodes:
    """These error codes should be commonly used for SQL related errors."""

    EXISTS = 'query.exists'
    REFERENCE_NOT_FOUND = 'query.reference_not_found'
    NOT_FOUND = 'query.not_found'
    INTERNAL_ERROR = 'query.internal_error'
    FIELD_DOES_NOT_EXISTS = 'query.field_does_not_exists'
    INVALID_CONDITION = 'query.invalid_condition_command'
    INVALID_ORDERING = 'query.invalid_ordering_command'
    INVALID_PAGINATION_OFFSET = 'query.invalid_pagination_offset'
    INVALID_PAGINATION_LIMIT = 'query.invalid_pagination_limit'
    INVALID_COLUMN = 'query.invalid_insert_column'


class SQLService(Service, abc.ABC):
    """Base SQL service interface with common commands and errors.

    Optimized for a single primary key only with a name "id"

    Example of use:

    You need to set your own table and, if needed, define column whitelists
    for different operations.

    .. code-block:: python

        class MyService(SQLService):
            table = my_table
            select_columns = {'id', 'data', 'flag'}
            insert_columns = {'data', 'flag'}
            update_columns = {'flag'}

    Here you can access some basic methods: "exists", "get", "create", "update",
    "delete" and their bulk versions (for multiple objects at once).

    Also there is a simply querying interface named "list"

    You can change any of SQL base for these commands by redefining query
    constructors.

    .. code-block:: python

        class MyService(SQLService):

            ...

            def _create_get_query(id, columns, table=None):
                ... # custom query

            def _create_m_get_query(self, id: list, columns, table=None):
                ... # custom query

    :param app: web app instance
    :param database_service: database service instance or instance name
    :param logger: optional logger instance
    """

    class _H_List(TypedDict):
        """Type hinting for a list query."""

        count: Optional[int]  #: total rows matching the query, None if count hasn't been requested
        offset: int  #: row offset for this selection
        page: Optional[int]  #: current page number, None if count hasn't been requested
        pages: Optional[int]  #: total pages, None if count hasn't been requested
        on_page: int  #: number of rows on this page
        data: Optional[List[dict]]  #: returned rows, None if limit was set to 0

    DEFAULT_ROW_LIMIT = 24  #: defaults of LIMIT on queries
    MAX_ROW_LIMIT = 1000  #: max size of queries

    select_columns = None  #: you can specify a whitelist of output columns here
    select_columns_blacklist = None
    update_columns = None  #: you may specify columns for update here
    update_columns_blacklist = None
    insert_columns = None  #: you may specify insert columns here
    insert_columns_blacklist = None
    table = None  #: here should be your table

    virtual_columns = None  # virtual SQL columns (i.e. functions) names and definitions
    # virtual columns can be selected but never updated / inserted

    def __init__(self, app, database_service: Union[DatabaseService, str] = None, logger=None):
        """Initialize."""

        def _prepare_whitelist(whitelist, blacklist):
            if blacklist:
                whitelist = set(col.name for col in self.table.columns) if whitelist is None else set(whitelist)
                return frozenset(whitelist.difference(set(blacklist)))
            elif whitelist:
                return frozenset(whitelist)

        Service.__init__(self, app=app, logger=logger)
        self._db = self.discover_service(database_service, cls=DatabaseService)
        self.table = self._db.add_table(self.table)  # registers table in the db service meta
        self._primary_keys = frozenset((col.name for col in self.table.primary_key))
        self._composite_primary_key = len(self._primary_keys) > 1
        if self._composite_primary_key:
            self._primary_key_condition = self._create_primary_key_condition_for_composite_key
            self._list_primary_key_condition = self._create_list_primary_key_condition_for_composite_key
            self._primary_key = self._primary_key_list = list(self.table.primary_key)
        elif len(self._primary_keys) == 1:
            self._primary_key_condition = self._create_primary_key_condition_for_single_key
            self._list_primary_key_condition = self._create_list_primary_key_condition_for_single_key
            self._primary_key = next(iter(self.table.primary_key))
            self._primary_key_list = [self._primary_key]
        else:
            self._primary_key_condition = self._raise_primary_key_condition_for_no_keys
            self._list_primary_key_condition = self._raise_primary_key_condition_for_no_keys
            self._primary_key = None
        self.select_columns = _prepare_whitelist(self.select_columns, self.select_columns_blacklist)
        self.insert_columns = _prepare_whitelist(self.insert_columns, self.insert_columns_blacklist)
        self.update_columns = _prepare_whitelist(self.update_columns, self.update_columns_blacklist)

    @property
    def routes(self) -> dict:
        """Get RPC routes."""
        return {
            'exists': self.exists,
            'get': self.get,
            'create': self.create,
            'update': self.update,
            'delete': self.delete,
            'm_exists': self.m_exists,
            'm_get': self.m_get,
            'm_create': self.m_create,
            'm_update': self.m_update,
            'm_delete': self.m_delete,
            'list': self.list,
        }

    @staticmethod
    def get_condition_hook(sql):
        """Set up specific get conditions."""
        return sql

    @staticmethod
    def insert_condition_hook(sql):
        """Set up specific insert conditions."""
        return sql

    @staticmethod
    def update_condition_hook(sql):
        """Set up specific update conditions."""
        return sql

    @staticmethod
    def delete_condition_hook(sql):
        """Set up specific delete conditions."""
        return sql

    def _create_primary_key_condition_for_single_key(self, sql, _id):
        return sql.where(self._primary_key == _id)

    def _create_list_primary_key_condition_for_single_key(self, sql, _id):
        if not isinstance(_id, (list, tuple, set)):
            _id = [_id]
        return sql.where(self._primary_key.in_(_id))

    def _parse_composite_id(self, _id):

        if not isinstance(_id, dict):
            raise ValidationError(
                message='Tables with composite primary keys'
                ' only support explicit id mappings with field names.'
                ' Expected an object in "id".',
                data={'id': '_id'},
            )

        conditions, col = [], None

        try:
            for col in self._primary_key:
                conditions.append(col == _id[col.name])
        except KeyError:
            raise ValidationError(
                message='Primary key field is not present in the primary key.', data={'id': _id, 'field': col.name}
            )
        return sa.and_(*conditions)

    def _create_list_primary_key_condition_for_composite_key(self, sql, _id):
        if not isinstance(_id, (list, tuple, set)):
            _id = [_id]
        condition = sa.or_(*(self._parse_composite_id(n) for n in _id))
        return sql.where(condition)

    def _create_primary_key_condition_for_composite_key(self, sql, _id: dict):
        condition = self._parse_composite_id(_id)
        return sql.where(condition)

    def _raise_primary_key_condition_for_no_keys(self, *_, **__):
        raise MethodNotAllowed(
            message='Direct referencing objects in the table is forbidden'
            ' because there are no primary keys in this table.'
        )

    async def _wrap_get(self, connection, sql):
        """Wrap a GET query to reraise SQL errors in a different format."""
        try:
            if connection:
                return await connection.execute(sql)
            else:
                async with self._db.connect() as connection:
                    return await connection.execute(sql)
        except Exception as exc:
            self.logger.debug('Internal error.', exc_info=exc)
            raise InternalError('Error processing query.', base_exc=exc, service=self.service_name)

    async def _wrap_insert(self, connection, sql):
        """Wrap an INSERT query to reraise SQL errors in a different format."""
        try:
            if connection:
                return await connection.execute(sql)
            else:
                async with self._db.begin() as connection:
                    return await connection.execute(sql)
        except IntegrityError as exc:
            raise Conflict(
                'Name conflict. Object already exists.',
                code=ErrorCodes.EXISTS,
                base_exc=exc,
                service=self.service_name,
            )
        except Exception as exc:
            self.logger.debug('Internal error.', exc_info=exc)
            raise InternalError(
                'Error processing query.', code=ErrorCodes.INTERNAL_ERROR, base_exc=exc, service=self.service_name
            )

    def _wrap_update(self, connection, sql):
        """Wrap an UPDATE query to reraise SQL errors in a different format."""
        return self._wrap_insert(connection, sql)

    def _wrap_delete(self, connection, sql):
        """Wrap a DELETE query to reraise SQL errors in a different format."""
        return self._wrap_insert(connection, sql)

    def _create_exists_query(self, _id, table=None):
        if table is None:
            table = self.table
        sql = table.select().with_only_columns(sa.text('1'))
        sql = self._primary_key_condition(sql, _id)
        sql = self.get_condition_hook(sql)
        sql = sql.limit(1)
        return sql

    async def exists(self, id, _connection=None) -> bool:
        """Return True if object exists. False otherwise.

        If you have composite primary keys you should pass dictionary objects
        in id field, like this:

        .. code-block:: python

            await service.exists({'id': 1, 'key': 'abc'})

        """
        sql = self._create_exists_query(id)
        result = await self._wrap_get(_connection, sql)
        return bool(result.first())

    def _create_m_exists_query(self, _id: list, table=None):
        if table is None:
            table = self.table
        sql = table.select().with_only_columns(*self._primary_key_list)
        sql = self._list_primary_key_condition(sql, _id)
        sql = self.get_condition_hook(sql)
        return sql

    async def m_exists(self, id: list, _connection=None):
        """Return a set of existing IDs for a list of IDs.

        If you have composite primary keys you should pass dictionary objects
        in id field, like this:

        .. code-block:: python

            await service.m_exists([{'id': 1, 'key': 'abc'}, ...])

        """
        sql = self._create_m_exists_query(id)
        result = await self._wrap_get(_connection, sql)
        rows = result.all()
        if rows:
            if self._composite_primary_key:
                result = [row._asdict() for row in rows]
                return result
            else:
                result = frozenset(next(iter(row._asdict().values())) for row in rows)
                return result
        else:
            return frozenset()

    def _sql_get_column(self, table, column: str):
        """Return an SQLAlchemy column by its name."""
        try:
            return self.table.columns[column]
        except KeyError:
            raise ValidationError(
                'Requested field doesn\'t exists',
                obj=table.name,
                field=column,
                service=self.service_name,
                code=ErrorCodes.FIELD_DOES_NOT_EXISTS,
            )

    def _sql_get_columns(self, columns, table=None) -> list:
        """Construct a list of columns from their names. By default it uses `self.table` as table.

        .. code-block:: python

            '*'             # all columns
            "..."           # single column
            ["...", "..."]  # multiple columns

        """
        if table is None:
            table = self.table

        if not columns:
            return []

        elif columns == '*':
            if self.select_columns is None:
                columns = self.table.columns
            else:
                columns = [col for col in self.table.columns if col.name in self.select_columns]
            if self.virtual_columns:
                virtual = [sa.text(value + f' AS {name}') for name, value in self.virtual_columns.items()]
                columns = [*columns, *virtual]
        else:
            if isinstance(columns, str):
                columns = [columns]

            if self.virtual_columns:

                _columns = []

                for column in columns:
                    if column in self.virtual_columns:
                        value = self.virtual_columns[column]
                        _columns.append(sa.text(value + f' AS {column}'))
                    elif self.select_columns:
                        if column in self.select_columns:
                            _columns.append(self._sql_get_column(table, column))
                    else:
                        _columns.append(self._sql_get_column(table, column))

                columns = _columns

            else:
                if self.select_columns:
                    columns = [self._sql_get_column(table, key) for key in columns if key in self.select_columns]
                else:
                    columns = [self._sql_get_column(table, key) for key in columns]

        return columns

    @staticmethod
    def _filter_columns(columns: List[sa.Column], whitelist: Optional[frozenset]):
        if whitelist is None:
            return columns
        else:
            return [col for col in columns if col.name in whitelist]

    def _create_get_query(self, _id, columns, table=None):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        sql = table.select().with_only_columns(*columns)
        sql = self._primary_key_condition(sql, _id)
        sql = self.get_condition_hook(sql)
        sql = sql.limit(1)
        return sql

    async def get(self, id, columns='*', _connection=None):
        """Return information about an object.

        If you have composite primary keys you should pass dictionary objects
        in id field, like this:

        .. code-block:: python

            await service.get({'id': 1, 'key': 'abc'}, ...)

        :raises NotFound:
        """
        if columns is None:
            raise ValidationError('Null "columns" param is not allowed in a get query.')

        sql = self._create_get_query(id, columns)
        result = await self._wrap_get(_connection, sql)
        result = result.first()
        if not result:
            raise NotFound(
                'Object doesn\'t exist.', service=self.service_name, object_id=str(id), code=ErrorCodes.NOT_FOUND
            )
        if columns:
            return result._asdict()

    def _create_m_get_query(self, _id: list, columns, table=None):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        sql = table.select().with_only_columns(*columns)
        sql = self._list_primary_key_condition(sql, _id)
        sql = self.get_condition_hook(sql)
        return sql

    async def m_get(self, id: list, columns='*', _connection=None):
        """Return multiple objects.

        Objects that don't exist will be skipped.
        Returns all data at once without pagination. Use `SQLService.list` if
        you want pagination or sorting.

        If you have composite primary keys you should pass dictionary objects
        in id field, like this:

        .. code-block:: python

            await service.m_get([{'id': 1, 'key': 'abc'}, ...], ...)

        """
        sql = self._create_m_get_query(id, columns)
        result = await self._wrap_get(_connection, sql)
        return [row._asdict() for row in result.all()]

    def _create_delete_query(self, _id, columns, table=None):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        sql = table.delete()
        sql = self._primary_key_condition(sql, _id)
        sql = self.delete_condition_hook(sql)
        if columns:
            sql = sql.returning(*columns)
        else:
            sql = sql.returning(sa.literal_column('1'))
        return sql

    async def delete(self, id, columns=None, _connection=None):
        """Remove a single object from a table.

        If you have composite primary keys you should pass dictionary objects
        in id field, like this:

        .. code-block:: python

            await service.delete({'id': 1, 'key': 'abc'}, ...)

        :raises NotFound: if object doesn't exist or already was deleted
        """
        sql = self._create_delete_query(id, columns)
        result = await self._wrap_delete(_connection, sql)
        result = result.first()
        if result is None:
            raise NotFound(
                'Object doesn\'t exist thus it can\'t be removed.',
                service=self.service_name,
                object_id=str(id),
                code=ErrorCodes.NOT_FOUND,
            )
        if columns:
            return result._asdict()

    def _create_m_delete_query(self, _id, conditions, columns, table=None):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        sql = table.delete()
        if _id:
            sql = self._list_primary_key_condition(sql, _id)
        if conditions:
            sql = self._create_conditions(sql, conditions, table)
        sql = self.delete_condition_hook(sql)
        sql = sql.returning(*columns)
        return sql

    async def m_delete(self, id: list = None, conditions=None, columns=None, _connection=None):
        """Remove multiple objects from a table. Non-existing objects will be skipped.

        If you have composite primary keys you should pass dictionary objects
        in id field, like this:

        .. code-block:: python

            await service.m_delete([{'id': 1, 'key': 'abc'}, ...], ...)

        """
        sql = self._create_m_delete_query(id, conditions, columns)
        result = await self._wrap_delete(_connection, sql)
        if columns:
            result = result.all()
            return [row._asdict() for row in result]

    @staticmethod
    def prepare_insert_data(data: dict):
        """Define your custom row init logic here."""
        return data

    def _validate_row(self, data: dict, whitelist: frozenset):
        """Validate and prepare insert row data."""
        if not data:
            raise ValidationError(
                'There are no columns for insert.',
                data=data,
                service=self.service_name,
                allowed_columns=self.insert_columns,
                code=ErrorCodes.INVALID_COLUMN,
            )

        if whitelist:
            if not set(data).issubset(whitelist):
                raise ValidationError(
                    'There are not consumed columns in the update statement.',
                    data=data,
                    service=self.service_name,
                    allowed_columns=self.insert_columns,
                    code=ErrorCodes.INVALID_COLUMN,
                )

    def _create_insert_query(self, data, columns, table=None, **on_conflict_clause):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        self._validate_row(data, whitelist=self.insert_columns)
        data = self.prepare_insert_data(data)
        sql = insert(table).values(data)
        sql = self._on_conflict_clause(sql, **on_conflict_clause)
        sql = self.insert_condition_hook(sql)
        sql = sql.returning(*columns)
        return sql

    def _on_conflict_clause(self, sql, on_conflict=None, on_conflict_keys=None, on_conflict_values=None):
        if on_conflict == 'do_nothing':
            sql = sql.on_conflict_do_nothing(index_elements=on_conflict_keys)
        elif on_conflict == 'do_update':
            if on_conflict_values:
                on_conflict_values = self.prepare_update_data(on_conflict_values)
            sql = sql.on_conflict_do_update(index_elements=on_conflict_keys, set_=on_conflict_values)
        return sql

    async def create(
        self,
        data: dict,
        columns='*',
        _connection=None,
        on_conflict=None,
        on_conflict_keys=None,
        on_conflict_values=None,
    ):
        """Create a single object.

        :param data: objects data
        :param columns: columns to return, None for no return
        :param on_conflict: on conflict clause if required ('do_nothing', 'do_update')
        :param on_conflict_keys: list of on conflict constraints
        :param on_conflict_values: an object with on conflict values, used only by `do_update` clause
        :returns: inserted object
        """
        sql = self._create_insert_query(
            data,
            columns,
            on_conflict=on_conflict,
            on_conflict_keys=on_conflict_keys,
            on_conflict_values=on_conflict_values,
        )
        result = await self._wrap_insert(_connection, sql)
        if columns:
            return result.first()._asdict()

    def _create_m_insert_query(self, data: List[dict], columns, table=None, **on_conflict_clause):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        _data = []
        for row in data:
            self._validate_row(row, whitelist=self.insert_columns)
            _data.append(self.prepare_insert_data(row))
        sql = insert(table).values(_data)
        sql = self._on_conflict_clause(sql, **on_conflict_clause)
        sql = self.insert_condition_hook(sql)
        sql = sql.returning(*columns)
        return sql

    async def m_create(
        self,
        data: List[dict],
        columns='*',
        _connection=None,
        on_conflict: str = None,
        on_conflict_keys: list = None,
        on_conflict_values: dict = None,
    ):
        """Create multiple objects.

        :param data: list of objects data
        :param columns: columns to return, None for no return
        :param on_conflict: on conflict clause if required ('do_nothing', 'do_update')
        :param on_conflict_keys: list of on conflict constraints
        :param on_conflict_values: an object with on conflict values, used only by `do_update` clause

        :returns: inserted objects
        """
        sql = self._create_m_insert_query(
            data,
            columns,
            on_conflict=on_conflict,
            on_conflict_keys=on_conflict_keys,
            on_conflict_values=on_conflict_values,
        )
        result = await self._wrap_insert(_connection, sql)
        if columns:
            return [row._asdict() for row in result.all()]

    @staticmethod
    def prepare_update_data(data: dict):
        """You may define your custom row update logic here."""
        return data

    def _create_update_query(self, _id, data: dict, columns, table=None):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        self._validate_row(data, whitelist=self.update_columns)
        data = self.prepare_update_data(data)
        sql = table.update().values(data)
        sql = self._primary_key_condition(sql, _id)
        sql = self.update_condition_hook(sql)
        sql = sql.returning(*columns) if columns else sql.returning(sa.literal_column('1'))
        return sql

    async def update(self, id, data: dict, columns='*', _connection=None) -> dict:
        """Update a single object. Raises error if object doesn't exist.

        If you have composite primary keys you should pass dictionary objects
        in id field, like this:

        .. code-block:: python

            await service.update({'id': 1, 'key': 'abc'}, ...)

        """
        sql = self._create_update_query(id, data, columns)
        result = await self._wrap_update(_connection, sql)
        result = result.first()
        if not result:
            raise NotFound(
                'Object doesn\'t exist thus it can\'t be updated.',
                service=self.service_name,
                object_id=str(id),
                code=ErrorCodes.NOT_FOUND,
            )
        if columns:
            return result._asdict()

    def _create_m_update_query(self, _id, data: dict, conditions, columns, table=None):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        self._validate_row(data, whitelist=self.update_columns)
        data = self.prepare_update_data(data)
        sql = table.update().values(data)
        if _id:
            sql = self._list_primary_key_condition(sql, _id)
        if conditions:
            sql = self._create_conditions(sql, conditions, table)
        sql = self.update_condition_hook(sql)
        sql = sql.returning(*columns)
        return sql

    async def m_update(self, id: list, data: dict, conditions=None, columns='*', _connection=None):
        """Update multiple objects with the same data. Non-existing objects will be skipped.

        If you have composite primary keys you should pass dictionary objects
        in id field, like this:

        .. code-block:: python

            await service.m_update([{'id': 1, 'key': 'abc'}, ...], ...)

        """
        sql = self._create_m_update_query(id, data, conditions, columns)
        result = await self._wrap_update(_connection, sql)
        if columns:
            return [row._asdict() for row in result.all()]

    def _create_conditions(self, sql, conditions, table=None):
        """Add SQL conditions to an sql query.

        Allows some simple queries to be constructed.

        .. code-block:: python

            [ ... ]  # OR
            { ... }  # AND

            { "...": "..." }            # ==
            { "...": ["...", "..."] }   # IN

        """
        if table is None:
            table = self.table

        def _get_conditions(condition):
            if type(condition) is dict:
                _condition = []
                for key, value in condition.items():
                    if self.select_columns and key not in self.select_columns:
                        raise ValidationError(
                            'Invalid condition requested. Unknown condition key.',
                            service=self.service_name,
                            key=key,
                            code=ErrorCodes.INVALID_CONDITION,
                        )

                    column = self._sql_get_column(table, key)
                    if type(value) is list:
                        _c = column.in_(value)
                    elif type(value) is dict:
                        _sub_cond = []
                        for key, _value in value.items():
                            key = key.lower()
                            if key == 'gt':
                                _sub_cond.append(column > _value)
                            elif key == 'lt':
                                _sub_cond.append(column < _value)
                            elif key == 'ge':
                                _sub_cond.append(column >= _value)
                            elif key == 'le':
                                _sub_cond.append(column <= _value)
                            elif key == 'eq':
                                _sub_cond.append(column == _value)
                            elif key == 'like':
                                _sub_cond.append(column.like(_value))
                            elif key == '~':
                                _sub_cond.append(sa.func.lower(column).op('~')(sa.func.lower(_value)))
                            elif key == 'not':
                                _sub_cond.append(sa.not_(column == _value))  # noqa
                            else:
                                raise ValidationError(
                                    'Invalid condition requested.',
                                    service=self.service_name,
                                    condition_key=key,
                                    code=ErrorCodes.INVALID_CONDITION,
                                )
                        _c = sa.and_(*_sub_cond)
                    else:
                        _c = column == value
                    _condition.append(_c)
                return sa.and_(*_condition)
            elif type(condition) is list:
                _condition = [_get_conditions(c) for c in condition]
                return sa.or_(*_condition)
            else:
                raise ValidationError(
                    'Invalid condition requested.' ' Condition must be an object or an array of objects.',
                    service=self.service_name,
                    code=ErrorCodes.INVALID_CONDITION,
                )

        conditions = _get_conditions(conditions)
        return sql.where(conditions)

    def _create_sort(self, sql, ordering, table=None):
        """Add SQL ordering command to a query.

        .. code-block:: python

            "..."            # sort ASC by a key
            {"desc": "..."}  # sort DESC by a key
            [ ..., ... ]     # sort by multiple keys in order

        """

        def _get_ordering(o):
            if isinstance(o, dict):
                key, name = next(iter(o.items()), None)
                key = key.lower()
            else:
                key = 'asc'
                name = o
            if type(name) is str:
                column = self._sql_get_column(table, name)
            else:
                column = name
            if key == 'desc':
                column = sa.desc(column)
            elif key == 'asc':
                pass
            else:
                raise ValidationError(
                    'Invalid ordering requested.',
                    service=self.service_name,
                    ordering_key=key,
                    code=ErrorCodes.INVALID_ORDERING,
                )
            return nullslast(column)

        if table is None:
            table = self.table
        if type(ordering) is list:
            sql = sql.order_by(*(_get_ordering(o) for o in ordering))
        else:
            sql = sql.order_by(_get_ordering(ordering))
        return sql

    def _create_pagination(self, sql, offset, limit):
        """Add pagination directives to an SQL query.

        Limit < 1 transforms to 1 and offset < 0 transforms to 0 by default.
        """
        if offset:
            try:
                offset = max(0, int(offset))
            except ValueError:
                raise ValidationError(
                    'Invalid offset.',
                    service=self.service_name,
                    pagination_key='offset',
                    value=offset,
                    code=ErrorCodes.INVALID_PAGINATION_OFFSET,
                )
            sql = sql.offset(offset)

        if limit is None:
            limit = self.DEFAULT_ROW_LIMIT

        try:
            limit = min(max(1, int(limit)), self.MAX_ROW_LIMIT)
        except ValueError:
            raise ValidationError(
                'Invalid limit.',
                service=self.service_name,
                pagination_key='limit',
                value=limit,
                code=ErrorCodes.INVALID_PAGINATION_LIMIT,
            )

        sql = sql.limit(limit)
        return sql

    def _create_count_query(self, conditions, precision=None, table=None):
        """Use COUNT(id) for slow precise count or TABLESAMPLE for estimate."""
        if table is None:
            table = self.table
        key = next(iter(self._primary_key_list))
        sql = table.select().with_only_columns(sa.func.count(key))
        if conditions:
            sql = self._create_conditions(sql, conditions, table=table)
        sql = self.get_condition_hook(sql)
        if precision:
            precision = min(max(1, precision), 100)
            sql = f'SELECT count({key.name})' f' FROM {table.name} TABLESAMPLE system({precision});'
        return sql

    def _create_list_query(self, conditions, sort, offset, limit, columns, table=None):
        if table is None:
            table = self.table
        columns = self._sql_get_columns(columns, table=table)
        sql = table.select().with_only_columns(*columns)
        if conditions:
            sql = self._create_conditions(sql, conditions, table=table)
        sql = self.get_condition_hook(sql)
        if sort:
            sql = self._create_sort(sql, sort, table=table)
        if offset or limit:
            sql = self._create_pagination(sql, offset, limit)
        return sql

    @staticmethod
    def _get_page_count(count: int, offset: int, page_size: int) -> (int, int):
        """Return current page number and number of pages."""
        if page_size:
            n = count - offset
            pages = max(1, count // page_size + bool(n % page_size))
            page = max(1, offset // page_size + bool(n % page_size))
            return page, pages
        else:
            return None, None

    async def list(
        self,
        conditions=None,
        sort=None,
        offset=0,
        limit=DEFAULT_ROW_LIMIT,
        count=True,
        precision=None,
        columns='*',
        _connection=None,
    ) -> _H_List:
        """List rows with pagination and conditions.

        Condition example:

        .. code-block:: python

            service.list(
                conditions={
                    'tag': ['tag_1', 'tag_2', 'tag_3']  # IN condition
                    'active': True                      # EQ condition
                    'value': {'gt': 41, 'le': 42'}      # num conditions,
                    'text': {'like': 'sht'}             # text field "likeness"
                }
            )

        Available numeric conditions: gt, lt, ge, le, eq
        Available other conditions: like

        Sort example:

        .. code-block:: python

            service.list(
                sort=['tag', {'desc': 'timestamp'}]     # order matters
            )

        Available sorting conditions: desc, asc (default)

        You can use this method for counting without returning any results.
        Just set the limit to zero. Optionally, you can also set the counting
        precision.

        .. code-block::

            service.list(
                conditions={ ... },
                precision=50
                limit=0
            )

        Contrary, if you don't need counting, you can disable it. No count / page
        data will be available then.

        .. code-block::

            service.list(
                conditions={ ... },
                count=False
            )

        Precision uses a number of table samples to estimate the count. If
        the precision is set to 0 or None, then the exact count will be performed.

        .. attention::

            Precision is not working at the moment (don't know why).

        If count argument is False, then count, page and pages result values
        will be None.

        If columns is None, then data will be None and on_page will be zero.

        :param conditions: optional query conditions
        :param sort: optional row ordering
        :param offset: optional row offset
        :param limit: optional row limit
        :param count: set to False to disable page counting
        :param precision: count precision, if None then table sampling won't be used
            must be from 0 to 100
        :param columns: columns to return
        :returns: dict
            This method may return different data depending on the provided params

        .. code-block:: python

            {
                count: Optional[int]          #: total rows matching the query, None if count hasn't been requested
                offset: int                   #: row offset for this selection
                page: Optional[int]           #: current page number, None if count hasn't been requested
                pages: Optional[int]          #: total pages, None if count hasn't been requested
                on_page: int                  #: number of rows on this page
                data: Optional[List[dict]]    #: returned rows, None if limit was set to 0
            }

        """
        if columns and limit:
            sql = self._create_list_query(conditions, sort, offset, limit, columns)
            result = await self._wrap_get(_connection, sql)
            result = result.all()
            result = [row._asdict() for row in result]
            if count:
                sql_count = self._create_count_query(conditions, precision)
                count = await self._wrap_get(_connection, sql_count)
                count = count.scalar()
                page, pages = self._get_page_count(count, offset, limit)
            else:
                count, page, pages = None, None, None
            on_page = len(result)
        else:
            on_page, result = 0, None
            if count:
                sql_count = self._create_count_query(conditions, precision)
                count = await self._wrap_get(_connection, sql_count)
                count = count.scalar()
                page, pages = self._get_page_count(count, offset, limit)
            else:
                count, page, pages, on_page = None, None, None, 0

        return {'count': count, 'offset': offset, 'page': page, 'pages': pages, 'on_page': on_page, 'data': result}

    async def iter(
        self, conditions=None, sort=None, offset=0, limit=DEFAULT_ROW_LIMIT, columns='*'
    ) -> AsyncGenerator[List[dict], None]:
        """Iterate over listed data.

        Almost the same as `SQLService.list` but returns a generator which iterates
        over the query content. It's not intended to be used by a client
        but inside the app or the service itself.

        See `SQLService.list` for info about params.
        """
        if not sort:
            sort = self._primary_key_list

        result = await self.list(
            conditions=conditions, sort=sort, offset=offset, limit=limit, columns=columns, count=True
        )

        page, pages = result['page'], result['pages']
        yield result['data']

        page += 1

        while page <= pages:
            offset = (page - 1) * limit
            result = await self.list(
                conditions=conditions, sort=sort, offset=offset, limit=limit, columns=columns, count=False
            )
            yield result['data']
            page += 1
