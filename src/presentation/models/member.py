from pydantic import BaseModel, EmailStr


class MemberInput(BaseModel):
    name: str
    email: EmailStr


class MemberUpdateInput(BaseModel):
    name: str | None = None
    email: str | None = None
