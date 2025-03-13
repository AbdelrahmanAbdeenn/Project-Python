from src.infrastructure.base_repo import BaseRepo
from src.domain.entities import Member
from src.infrastructure.database.schema import members

class MemberRepo(BaseRepo[Member]):
    def __init__(self) -> None:
        super().__init__(Member, members, 'member_id')

