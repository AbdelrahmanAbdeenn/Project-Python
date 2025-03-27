from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from src.application.book_services import BookServices
from src.domain.book_entity import Book

router = APIRouter()
book_services = BookServices()


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


@router.get('/book')
def get_all() -> list[Book]:
    books = book_services.get(None)
    if isinstance(books, list):
        return books
    else:
        return [books]
    return [b for b in books]


@router.get('/book/{id}')
def get_by_id(id: int) -> Book | list[Book]:
    book = book_services.get(id)
    return book


@router.post('/book')
def create_book(book_data: BookInput) -> Book:
    book = book_services.create(vars(book_data))
    return book


@router.patch('/book/{id}')
def update_book(id: int, book_data: BookUpdateInput) -> Book:
    data = book_data.model_dump(
        exclude_none=True
    )
    book = book_services.update(id, data)
    return book


@router.delete('/book/{id}')
def delete_book(id: int) -> dict[str, str]:
    return book_services.delete(id)
