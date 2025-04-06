from datetime import datetime

from pydantic import BaseModel


class BookInput(BaseModel):
    title: str
    author: str
    is_borrowed: bool | None = False
    borrowed_date: datetime | None = None
    borrowed_by: str | None = None


class BookUpdateInput(BaseModel):
    title: str | None = None
    author: str | None = None
    is_borrowed: bool | None = None
    borrowed_date: datetime | None = None
    borrowed_by: str | None = None
