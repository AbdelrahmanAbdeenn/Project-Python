from fastapi import APIRouter

from src.application.book_services import BookServices
from src.domain.book_entity import Book
from src.presentation.models.book import BookInput, BookUpdateInput

router = APIRouter()
book_services = BookServices()


@router.get('/book', response_model=list[Book])
async def get_all() -> list[Book]:
    books = await book_services.get(None)
    if isinstance(books, list):
        return books
    else:
        return [books]


@router.get('/book/{id}')
async def get_by_id(id: int) -> Book | list[Book]:
    book = await book_services.get(id)
    return book


@router.post('/book')
async def create_book(book_data: BookInput) -> Book:
    book = await book_services.create(vars(book_data))
    return book


@router.patch('/book/{id}')
async def update_book(id: int, book_data: BookUpdateInput) -> Book:
    data = book_data.model_dump(
        exclude_none=True
    )
    book = await book_services.update(id, data)
    return book


@router.delete('/book/{id}')
async def delete_book(id: int) -> dict[str, str]:
    return await book_services.delete(id)
