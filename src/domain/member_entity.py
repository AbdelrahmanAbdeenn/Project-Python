from src.domain.base_entity import BaseEntity


class Member(BaseEntity):
    member_id: int
    name: str
    email: str

    def __init__(self, name: str, email: str, member_id: int) -> None:
        self.member_id = member_id
        self.name = name
        self.email = email
