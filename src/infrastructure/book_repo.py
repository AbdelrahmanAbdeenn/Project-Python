from src.domain.book_entity import Book
from src.infrastructure.base_repo import BaseRepo
from src.infrastructure.database.schema import books


class BookRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(Book, books, 'book_id')
