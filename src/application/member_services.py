from src.application.base_services import BaseServices
from src.domain.member_entity import Member
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.repositories.member_repo import MemberRepo


class MemberServices(BaseServices[Member]):
    def __init__(self) -> None:
        uow = UnitOfWork()
        super().__init__(MemberRepo(), uow)

    async def get(self, id: int | None | str) -> list[Member] | Member:
        async with self.uow:
            if id is None:
                return await self.repo.get_all(self.uow.connection)

            entity = await self.repo.get_by_id(id, self.uow.connection)
            if not entity:
                raise ValueError('Entity not found')
            return entity
