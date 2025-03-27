from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from src.application.member_services import MemberServices
from src.domain.member_entity import Member

member_services = MemberServices()
router = APIRouter()


class MemberInput(BaseModel):
    name: str
    email: EmailStr


class MemberUpdateInput(BaseModel):
    name: str | None = None
    email: str | None = None


@router.get('/member')
def get_all() -> list[Member]:
    members = member_services.get(None)
    if isinstance(members, list):
        return members
    else:
        return [members]


@router.get('/member/{id}')
def get_by_id(id: str) -> Member | list[Member]:
    member = member_services.get(id)
    return member


@router.post('/member')
def create_member(member_data: MemberInput) -> Member:
    member = member_services.create(vars(member_data))
    return member


@router.patch('/member/{id}')
def update_member(id: str, member_data: MemberUpdateInput) -> Member:
    data = member_data.model_dump(
        exclude_none=True
    )
    member = member_services.update(id, data)
    return member


@router.delete('/member/{id}')
def delete(id: str) -> dict[str, str]:
    return member_services.delete(id)
