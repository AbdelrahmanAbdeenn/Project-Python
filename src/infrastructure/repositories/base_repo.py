from typing import Any, Generic, Type, TypeVar

from sqlalchemy import Connection, Table, delete, insert, select, update

from src.domain.base_entity import BaseEntity

E = TypeVar("E", bound=BaseEntity)


class BaseRepo(Generic[E]):
    def __init__(self, entity_type: Type[E], table: Table) -> None:
        self.entity_type = entity_type
        self.table = table

    def get_all(self, connection: Connection) -> list[E]:
        statement = select(self.table)
        result = connection.execute(statement).fetchall()
        return [self._map_row_to_entity(row) for row in result]

    def get_by_id(self, id: int | str, connection: Connection) -> E | None:
        statement = select(self.table).where(self.table.c.id == id)
        result = connection.execute(statement).fetchone()
        if result:
            return self._map_row_to_entity(result)
        return None

    def add(self, connection: Connection, entity: E) -> E:
        entity_dict = vars(entity)
        primary_column_key = list(self.table.c)[0]
        entity_dict.pop('id', None)
        entity_dict.pop('books', None)
        statement = insert(self.table).values(entity_dict).returning(primary_column_key)
        result = connection.execute(statement)
        new_id = result.scalar_one()
        setattr(entity, primary_column_key.name, new_id)
        return entity

    def update(self, connection: Connection, id: int | str, data: Any) -> bool:
        statement = update(self.table).where(self.table.c.id == id).values(data)
        result = connection.execute(statement)
        return result.rowcount > 0

    def delete(self, id: int | str, connection: Connection) -> bool:
        statement = delete(self.table).where(self.table.c.id == id)
        result = connection.execute(statement)
        return result.rowcount > 0

    def _map_row_to_entity(self, row: Any) -> E:
        row_dict = dict(row._mapping)
        return self.entity_type(**row_dict)
