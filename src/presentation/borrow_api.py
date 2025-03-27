from fastapi import APIRouter

from src.application.book_services import BookServices

router = APIRouter()
bookServices = BookServices()


@router.post('/borrow/{book_id}/{member_id}')
def post(book_id: int, member_id: str) -> dict[str, str]:
    return bookServices.borrow_book(book_id, member_id)
