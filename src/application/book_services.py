from datetime import datetime
from typing import Any, Dict

from sqlalchemy.orm import Session

from src.application.base_services import BaseServices
from src.domain.book_entity import Book
from src.infrastructure.book_repo import BookRepo
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.member_repo import MemberRepo


class BookServices(BaseServices[Book]):
    def __init__(self) -> None:
        super().__init__(BookRepo(), UnitOfWork())
        self.member_repo = MemberRepo()

    def borrow_book(self, book_id: int, member_id: int) -> Dict[str, str]:
        with self.uow:
            session = self.uow.get_session()
            book = self._get_book_by_id(book_id, session)
            self._validate_book_availability(book)
            self._get_member_by_id(member_id, session)

            self.repo.update(session, book_id, {
                "is_borrowed": True,
                "borrowed_by": member_id,
                "borrowed_date": datetime.today()
            })
            return {"message": "Book borrowed successfully"}

    def return_book(self, book_id: int) -> Dict[str, str]:
        with self.uow:
            session = self.uow.get_session()
            book = self._get_book_by_id(book_id, session)
            if not book.is_borrowed:
                raise ValueError("Book is not currently borrowed")

            self.repo.update(session, book_id, {
                "is_borrowed": False,
                "borrowed_by": None,
                "borrowed_date": None
            })
            return {"message": "Book returned successfully"}

    def _validate_book_availability(self, book: Book) -> None:
        if book.is_borrowed:
            raise ValueError(
                f"Book is already borrowed by member {book.borrowed_by} "
                f"since {book.borrowed_date.strftime('%Y-%m-%d %H:%M:%S') if book.borrowed_date else 'Unknown date'}"
            )

    def _get_book_by_id(self, book_id: int, session: Session) -> Book:
        book = self.repo.get_by_id(book_id, session)
        if not book:
            raise ValueError("Book not found")
        return book

    def _get_member_by_id(self, member_id: int, session: Session) -> Any:
        member = self.member_repo.get_by_id(member_id, session)
        if not member:
            raise ValueError("Member not found")
        return member
