from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncConnection

from src.application.base_services import BaseServices
from src.domain.book_entity import Book
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.repositories.book_repo import BookRepo
from src.infrastructure.repositories.member_repo import MemberRepo


class BookServices(BaseServices[Book]):
    def __init__(self) -> None:
        super().__init__(BookRepo(), UnitOfWork())
        self.member_repo = MemberRepo()

    async def borrow_book(self, id: int, member_id: str) -> dict[str, str]:
        async with self.uow:
            book = await self._get_book_by_id(id, self.uow.connection)
            self._validate_book_availability(book)
            await self._get_member_by_id(member_id, self.uow.connection)

            await self.repo.update(self.uow.connection, id, {
                'is_borrowed': True,
                'borrowed_by': member_id,
                'borrowed_date': datetime.today()
            })
            return {'message': 'Book borrowed successfully'}

    async def return_book(self, id: int) -> Book:
        async with self.uow:
            book = await self._get_book_by_id(id, self.uow.connection)
            if not book.is_borrowed:
                raise ValueError('Book is not currently borrowed')

            await self.repo.update(self.uow.connection, id, {
                'is_borrowed': False,
                'borrowed_by': None,
                'borrowed_date': None
            })
            return await self._get_book_by_id(id, self.uow.connection)

    def _validate_book_availability(self, book: Book) -> None:
        if book.is_borrowed:
            raise ValueError(
                f"Book is already borrowed by member {book.borrowed_by} "
                f"since {book.borrowed_date.strftime('%Y-%m-%d %H:%M:%S') if book.borrowed_date else 'Unknown date'}")

    async def _get_book_by_id(self, book_id: int, connection: AsyncConnection) -> Book:
        book = await self.repo.get_by_id(book_id, connection)
        if not book:
            raise ValueError('Entity not found')
        return book

    async def _get_member_by_id(self, member_id: str, connection: AsyncConnection) -> Any:
        member = await self.member_repo.get_by_id(member_id, connection)
        if not member:
            raise ValueError('Member not found')
        return member
