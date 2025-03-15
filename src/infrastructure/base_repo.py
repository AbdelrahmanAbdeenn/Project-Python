from typing import Any, Generic, List, Type, TypeVar

from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.orm import Session

from src.domain.base_entity import BaseEntity

E = TypeVar('E', bound='BaseEntity')


class BaseRepo(Generic[E]):
    def __init__(self, entity_type: Type[E], table: Table, primary_key_column: str) -> None:
        self.entity_type = entity_type
        self.table = table
        self.primary_key_column = primary_key_column

    def get_all(self, session: Session) -> List[E]:
        statement = select(self.table)
        result = session.execute(statement).fetchall()
        entities = []
        for row in result:
            entity = self._map_row_to_entity(row)
            entities.append(entity)
        return entities

    def get_by_id(self, id: int, session: Session) -> E | None:
        statement = select(self.table).where(getattr(self.table.c, self.primary_key_column) == id)
        result = session.execute(statement).fetchone()
        if result:
            return self._map_row_to_entity(result)
        return None

    def add(self, session: Session, entity: E) -> E:
        entity_dict = vars(entity)
        primary_key_column = self.table.primary_key.columns.keys()[0]
        if 'id' in entity_dict:
            entity_dict[primary_key_column] = entity_dict.pop('id')
        statement = insert(self.table).values(entity_dict)
        session.execute(statement)
        return entity

    def update(self, session: Session, id: int, data: Any) -> bool:
        statement = update(self.table).where(getattr(self.table.c, self.primary_key_column) == id).values(data)
        result = session.execute(statement)
        return result.rowcount > 0

    def delete(self, id: int, session: Session) -> bool:
        statement = delete(self.table).where(getattr(self.table.c, self.primary_key_column) == id)
        result = session.execute(statement)
        return result.rowcount > 0

    def _map_row_to_entity(self, row: Any) -> E:
        row_dict = dict(row._mapping)
        primary_key_column = self.primary_key_column
        if "id" in row_dict:
            row_dict[primary_key_column] = row_dict.pop("id")
        entity = self.entity_type(**row_dict)
        return entity
