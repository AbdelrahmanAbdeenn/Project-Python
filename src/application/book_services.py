from src.application.base_services import BaseServices
from src.domain.entities import Book
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.book_repo import BookRepo
from src.infrastructure.member_repo import MemberRepo
from datetime import datetime
from werkzeug.exceptions import NotFound, BadRequest

class BookServices(BaseServices[Book]):
    def __init__(self):
        super().__init__(BookRepo(), UnitOfWork())
        self.member_repo = MemberRepo()

    def borrow_book(self, book_id: int, member_id: int):
        with self.uow:  
            session = self.uow.get_session()
            book = self.repo.get_by_id(book_id, session)
            self._validate_book_availability(book)
            member = self.member_repo.get_by_id(member_id, session)
            self._validate_member_exists(member)

            self.repo.update(session, book_id, {
                'is_borrowed': True,
                'borrowed_by': member_id,
                'borrowed_date': datetime.today()
            })
            return {"message": "Book borrowed successfully"}, 200

    def return_book(self, book_id: int):
        with self.uow:
            session = self.uow.get_session()
            book = self.repo.get_by_id(book_id, session)
            if not book:
                raise ValueError("Book not found")
            if not book.is_borrowed:
                raise ValueError("Book is not currently borrowed")

            self.repo.update(session, book_id, {
                'is_borrowed': False,
                'borrowed_by': None,
                'borrowed_date': None
            })
            return {"message": "Book returned successfully"}, 200
        
    def _validate_book_availability(self, book):
        if not book:
            raise ValueError("Book not found")
        if book.is_borrowed:
            raise ValueError(f"Book is already borrowed by member {book.borrowed_by} since {book.borrowed_date.strftime('%Y-%m-%d %H:%M:%S')}")

    def _validate_member_exists(self, member):
        if not member:
            raise ValueError("Member not found")