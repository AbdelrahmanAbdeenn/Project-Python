from typing import Any, Generic, Type, TypeVar

from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from src.domain.base_entity import BaseEntity

E = TypeVar("E", bound=BaseEntity)


class BaseRepo(Generic[E]):
    def __init__(self, entity_type: Type[E], table: Table) -> None:
        self.entity_type = entity_type
        self.table = table

    async def get_all(self, connection: AsyncConnection) -> list[E]:
        statement = select(self.table)
        result = await connection.execute(statement)
        rows = result.all()
        return [self._map_row_to_entity(row) for row in rows]

    async def get_by_id(self, id: int | str, connection: AsyncConnection) -> E | None:
        statement = select(self.table).where(self.table.c.id == id)
        result = await connection.execute(statement)
        row = result.first()
        if result:
            return self._map_row_to_entity(row)
        return None

    async def add(self, connection: AsyncConnection, entity: E) -> E:
        entity_dict = vars(entity)
        primary_column_key = list(self.table.c)[0]
        entity_dict.pop('id', None)
        entity_dict.pop('books', None)
        statement = insert(self.table).values(entity_dict).returning(primary_column_key)
        result = await connection.execute(statement)
        new_id = result.scalar_one()
        setattr(entity, primary_column_key.name, new_id)
        return entity

    async def update(self, connection: AsyncConnection, id: int | str, data: Any) -> bool:
        statement = update(self.table).where(self.table.c.id == id).values(data)
        result = await connection.execute(statement)
        return result.rowcount > 0

    async def delete(self, id: int | str, connection: AsyncConnection) -> bool:
        statement = delete(self.table).where(self.table.c.id == id)
        result = await connection.execute(statement)
        return result.rowcount > 0

    def _map_row_to_entity(self, row: Any) -> E:
        row_dict = dict(row._mapping)
        return self.entity_type(**row_dict)
