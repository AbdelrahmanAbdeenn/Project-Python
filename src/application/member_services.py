from src.application.base_services import BaseServices
from src.domain.member_entity import Member
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.member_repo import MemberRepo


class MemberServices(BaseServices[Member]):
    def __init__(self) -> None:
        uow = UnitOfWork()
        super().__init__(MemberRepo(), uow)
