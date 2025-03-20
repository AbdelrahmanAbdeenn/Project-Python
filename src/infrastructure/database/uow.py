from types import TracebackType
from typing import Any, Type

from sqlalchemy import Connection, Result, Transaction

from src.infrastructure.database.db import engine


class UnitOfWork:
    def __init__(self) -> None:
        self._connection: Connection | None = None
        self._transaction: Transaction | None = None

    def __enter__(self) -> 'UnitOfWork':
        self._connection = engine.connect()
        self._transaction = self._connection.begin()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._transaction is None:
            raise RuntimeError('Transaction not initialized')

        if exc_type is None:
            self._transaction.commit()
        else:
            self._transaction.rollback()

    @property
    def connection(self) -> Connection:
        if self._connection is None:
            raise RuntimeError('Connection not initialized')
        return self._connection

    def execute(self, statement: Any) -> Result[Any]:
        return self.connection.execute(statement)

    def fetchone(self, statement: Any) -> Any:
        result = self.execute(statement)
        return result.fetchone()

    def fetchall(self, statement: Any) -> Any:
        result = self.execute(statement)
        return result.fetchall()
