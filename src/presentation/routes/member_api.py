from fastapi import APIRouter

from src.application.member_services import MemberServices
from src.domain.member_entity import Member
from src.presentation.models.member import MemberInput, MemberUpdateInput

member_services = MemberServices()
router = APIRouter(tags=['Member'])


@router.get('/member')
async def get_all() -> list[Member]:
    members = await member_services.get(None)
    if isinstance(members, list):
        return members
    else:
        return [members]


@router.get('/member/{id}')
async def get_by_id(id: str) -> Member | list[Member]:
    member = await member_services.get(id)
    return member


@router.post('/member')
async def create_member(member_data: MemberInput) -> Member:
    member = await member_services.create(vars(member_data))
    return member


@router.patch('/member/{id}')
async def update_member(id: str, member_data: MemberUpdateInput) -> Member:
    data = member_data.model_dump(
        exclude_none=True
    )
    member = await member_services.update(id, data)
    return member


@router.delete('/member/{id}')
async def delete(id: str) -> dict[str, str]:
    return await member_services.delete(id)
