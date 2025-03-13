# from typing import TypeVar, Generic, Any, Union
# from sqlalchemy.exc import IntegrityError
# from werkzeug.exceptions import NotFound, BadRequest, InternalServerError
# from src.domain.entities import BaseEntity
# from src.infrastructure.base_repo import BaseRepo
# from src.infrastructure.database.uow import UnitOfWork

# E = TypeVar('E', bound='BaseEntity')

# class BaseServices(Generic[E]):
#     def __init__(self, repo: BaseRepo[E], uow: UnitOfWork):
#         self.repo = repo
#         self.uow = uow

#     def get(self, id: int | None) -> Union[list[E], E]:
#         with self.uow:
#             session = self.uow.get_session()
#             if id is None:
#                 entities = self.repo.get_all(session)
#                 return [vars(entity) for entity in entities]
#             else:
#                 entity = self.repo.get_by_id(id, session)
#                 if entity is None:
#                     raise NotFound("Entity not found")
#                 return vars(entity)

#     def create(self, data: Any) -> Any:
#         with self.uow:
#             session = self.uow.get_session()
#             try:
#                 entity: E = self.repo.entity_type(**data)
#                 if not entity:
#                     raise BadRequest("Entity creation failed")
                
#                 if self.repo.get_by_id(entity.id, session):
#                     raise BadRequest("Entity with this ID already exists")
                
#                 self.repo.add(session, entity)
#                 return vars(entity)
#             except IntegrityError:
#                 raise BadRequest("Duplicate entry, entity already exists")
#             except Exception as e:
#                 raise InternalServerError(str(e))

#     def update(self, id: int, data: Any):
#         with self.uow:
#             session = self.uow.get_session()
#             entity = self.repo.get_by_id(id, session)
#             if not entity:
#                 raise NotFound("Entity not found")
#             updated = self.repo.update(session, id, data)
#             new_entity = self.repo.get_by_id(id, session)
#             if not updated:
#                 raise BadRequest("Failed to update entity")
#             return vars(new_entity)

#     def delete(self, id: int):
#         with self.uow:
#             session = self.uow.get_session()
#             entity = self.repo.get_by_id(id, session)
#             if entity is None:
#                 raise NotFound("Entity not found")
#             deleted = self.repo.delete(id, session)
#             if not deleted:
#                 raise BadRequest("Failed to delete entity")
#             return {"message": "Entity deleted successfully"}

from typing import TypeVar, Generic, Any, Union
from sqlalchemy.exc import IntegrityError
from src.domain.entities import BaseEntity
from src.infrastructure.base_repo import BaseRepo
from src.infrastructure.database.uow import UnitOfWork

E = TypeVar('E', bound='BaseEntity')

class BaseServices(Generic[E]):
    def __init__(self, repo: BaseRepo[E], uow: UnitOfWork):
        self.repo = repo
        self.uow = uow


    def get(self, id: int | None) -> Union[list[E], E, dict[str, Any]]:
        with self.uow:
            session = self.uow.get_session()
            if id is None:
                entities = self.repo.get_all(session)
                return [vars(entity) for entity in entities]
            else:
                entity = self._get_entity(id, session)
                return vars(entity)
    
    def create(self, data: Any) -> Any:
        with self.uow:
            session = self.uow.get_session()
            try:
                entity: E = self.repo.entity_type(**data)
                self._validate_creation(entity, session)
                self.repo.add(session, entity)
                return vars(entity)
            except IntegrityError:
                raise ValueError("Duplicate entry, entity already exists")
            except Exception as e:
                raise ValueError(str(e))

    def update(self, id: int, data: Any):
        with self.uow:
            session = self.uow.get_session()
            self._get_entity(id, session)
            if not self.repo.update(session, id, data):
                raise ValueError("Failed to update entity")
            return vars(self._get_entity(id, session))

    def delete(self, id: int):
        with self.uow:
            session = self.uow.get_session()
            self._get_entity(id, session)
            if not self.repo.delete(id, session):
                raise ValueError("Failed to delete entity")
            return {"message": "Entity deleted successfully"}
        
    def _get_entity(self, id: int, session) -> E:
        entity = self.repo.get_by_id(id, session)
        if not entity:
            raise ValueError("Entity not found")
        return entity

    def _validate_creation(self, entity: E, session):
            if not entity:
                raise ValueError("Entity creation failed")
            primary_key_column = self.repo.primary_key_column  # Get correct primary key
            entity_id = getattr(entity, primary_key_column, None)
            if entity_id and self.repo.get_by_id(entity_id, session):
                raise ValueError(f"Entity with this {primary_key_column} already exists")
