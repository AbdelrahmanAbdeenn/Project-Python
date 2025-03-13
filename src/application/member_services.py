from src.application.base_services import BaseServices
from src.domain.entities import Member
from src.infrastructure.member_repo import MemberRepo
from src.infrastructure.database.uow import UnitOfWork

class MemberServices(BaseServices[Member]):
    def __init__(self):
        uow = UnitOfWork()
        super().__init__(MemberRepo(),uow)
