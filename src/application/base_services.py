from typing import Any, Generic, List, TypeVar, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.domain.base_entity import BaseEntity
from src.infrastructure.base_repo import BaseRepo
from src.infrastructure.database.uow import UnitOfWork

E = TypeVar('E', bound=BaseEntity)


class BaseServices(Generic[E]):
    def __init__(self, repo: BaseRepo[E], uow: UnitOfWork) -> None:
        self.repo = repo
        self.uow = uow

    def get(self, id: Union[int, None]) -> Union[List[E], E]:
        with self.uow:
            session = self.uow.get_session()
            if id is None:
                return self.repo.get_all(session)  # Returns List[E]
            else:
                return self._get_entity(id, session)  # Returns E

    def create(self, data: dict[str, Any]) -> E:
        with self.uow:
            session = self.uow.get_session()
            try:
                entity: E = self.repo.entity_type(**data)
                self._validate_creation(entity, session)
                self.repo.add(session, entity)
                return entity  # ✅ Return the actual entity instead of a dict
            except IntegrityError:
                raise ValueError("Duplicate entry, entity already exists")
            except Exception as e:
                raise ValueError(str(e))

    def update(self, id: int, data: dict[str, Any]) -> E:
        with self.uow:
            session = self.uow.get_session()
            self._get_entity(id, session)
            if not self.repo.update(session, id, data):
                raise ValueError("Failed to update entity")
            return self._get_entity(id, session)

    def delete(self, id: int) -> dict[str, str]:
        with self.uow:
            session = self.uow.get_session()
            self._get_entity(id, session)
            if not self.repo.delete(id, session):
                raise ValueError("Failed to delete entity")
            return {"message": "Entity deleted successfully"}

    def _get_entity(self, id: int, session: Session) -> E:
        entity = self.repo.get_by_id(id, session)
        if not entity:
            raise ValueError("Entity not found")
        return entity

    def _validate_creation(self, entity: E, session: Session) -> None:
        if not entity:
            raise ValueError("Entity creation failed")
        primary_key_column: str = self.repo.primary_key_column
        entity_id = getattr(entity, primary_key_column, None)
        if entity_id and self.repo.get_by_id(entity_id, session):
            raise ValueError(f"Entity with this {primary_key_column} already exists")
