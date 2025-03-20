from typing import Any, Generic, TypeVar

from sqlalchemy import Connection

from src.domain.base_entity import BaseEntity
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.repositories.base_repo import BaseRepo

E = TypeVar("E", bound=BaseEntity)


class BaseServices(Generic[E]):
    def __init__(self, repo: BaseRepo[E], uow: UnitOfWork) -> None:
        self.repo = repo
        self.uow = uow

    def get(self, id: int | None | str) -> list[E] | E:
        with self.uow:
            if id is None:
                return self.repo.get_all(self.uow.connection)

            return self._get_entity(id, self.uow.connection)

    def create(self, data: dict[str, Any]) -> E:
        with self.uow:
            try:
                entity: E = self.repo.entity_type(**data)
                self.repo.add(self.uow.connection, entity)
                return entity

            except Exception as e:
                raise ValueError(str(e))

    def update(self, id: int | str, data: dict[str, Any]) -> E:
        with self.uow:
            if not self.repo.update(self.uow.connection, id, data):
                raise ValueError('Failed to update entity')
            return self._get_entity(id, self.uow.connection)

    def delete(self, id: int | str) -> dict[str, str]:
        with self.uow:
            if not self.repo.delete(id, self.uow.connection):
                raise ValueError('Failed to delete entity')
            return {'message': 'Entity deleted successfully'}

    def _get_entity(self, id: int | str, connection: Connection) -> E:
        entity = self.repo.get_by_id(id, connection)
        if not entity:
            raise ValueError('Entity not found')
        return entity

    def _validate_creation(self, entity: E, connection: Connection) -> None:
        if not entity:
            raise ValueError('Entity creation failed')
