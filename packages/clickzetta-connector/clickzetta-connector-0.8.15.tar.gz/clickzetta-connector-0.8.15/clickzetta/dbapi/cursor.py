"""Cursor for ClickZetta DB-API."""

import collections
import logging
from clickzetta.query_result import QueryResult

_LOGGER = logging.getLogger(__name__)

Column = collections.namedtuple(
    "Column",
    [
        "name",
        "type_code",
        "display_size",
        "internal_size",
        "precision",
        "scale",
        "null_ok",
    ],
)


class Cursor(object):
    def __init__(self, connection):
        self.connection = connection
        self.description = None
        self.rowcount = -1
        self._query_result = None
        self._query_data = None
        self._closed = False

    def close(self):
        self._closed = True

    def _set_rowcount(self, query_result):

        self.rowcount = query_result.total_row_count

    def _set_description(self, query_result: QueryResult):
        if query_result.schema is None:
            self.description = None
            return

        self.description = tuple(
            Column(
                name=field.name,
                type_code=field.field_type,
                display_size=None,
                internal_size=field.length,
                precision=field.precision,
                scale=field.scale,
                null_ok=field.nullable,
            )
            for field in query_result.schema
        )

    def execute(self, operation: str, parameters=None):

        self._execute(operation, parameters)

    def _execute(
            self, operation: str, parameters
    ):
        if operation is None:
            raise ValueError("sql is empty")
        else:
            operation = operation.strip()
            if operation == "":
                raise ValueError("sql is empty")
        self._query_data = None
        self._query_job = None
        client = self.connection._client
        operation = operation + ";" if not operation.endswith(";") else operation

        self._query_result = client.submit_sql_job(token=client.token, sql=operation, parameters=parameters)
        self._set_rowcount(self._query_result)
        self._query_data = self._query_result.data
        self._set_description(self._query_result)

    def executemany(self, operations, methods):
        print("not supported yet")

    def fetchone(self):
        try:
            return self._query_data.fetch_one()
        except StopIteration:
            return None

    def fetchmany(self, size=None):
        try:
            return self._query_data.fetch_many(size)
        except StopIteration:
            return None

    def fetchall(self):
        return self._query_data.fetch_all()

    def setinputsizes(self, sizes):
        """No-op, but for consistency raise an error if cursor is closed."""

    def setoutputsize(self, size, column=None):
        """No-op, but for consistency raise an error if cursor is closed."""

    def __iter__(self):
        return iter(self._query_data)
