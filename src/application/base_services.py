from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncConnection

from src.domain.base_entity import BaseEntity
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.repositories.base_repo import BaseRepo

E = TypeVar("E", bound=BaseEntity)


class BaseServices(Generic[E]):
    def __init__(self, repo: BaseRepo[E], uow: UnitOfWork) -> None:
        self.repo = repo
        self.uow = uow

    async def get(self, id: int | None | str) -> list[E] | E:
        async with self.uow:
            if id is None:
                return await self.repo.get_all(self.uow.connection)

            return await self._get_entity(id, self.uow.connection)

    async def create(self, data: dict[str, Any]) -> E:
        async with self.uow:
            try:
                entity: E = self.repo.entity_type(**data)
                await self.repo.add(self.uow.connection, entity)
                return entity

            except Exception as e:
                raise ValueError(str(e))

    async def update(self, id: int | str, data: dict[str, Any]) -> E:
        async with self.uow:
            if not await self.repo.update(self.uow.connection, id, data):
                raise ValueError('Failed to update entity')
            return await self._get_entity(id, self.uow.connection)

    async def delete(self, id: int | str) -> dict[str, str]:
        async with self.uow:
            if not await self.repo.delete(id, self.uow.connection):
                raise ValueError('Failed to delete entity')
            return {'message': 'Entity deleted successfully'}

    async def _get_entity(self, id: int | str, connection: AsyncConnection) -> E:
        entity = await self.repo.get_by_id(id, connection)
        if not entity:
            raise ValueError('Entity not found')
        return entity

    def _validate_creation(self, entity: E, connection: AsyncConnection) -> None:
        if not entity:
            raise ValueError('Entity creation failed')
