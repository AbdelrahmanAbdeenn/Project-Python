from fastapi import APIRouter

from src.application.book_services import BookServices
from src.domain.book_entity import Book

router = APIRouter()
book_services = BookServices()


@router.post('/return/{book_id}')
def return_book(id: int) -> Book:
    return book_services.return_book(id)
