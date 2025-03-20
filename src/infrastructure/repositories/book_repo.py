from src.domain.book_entity import Book
from src.infrastructure.database.schema import books
from src.infrastructure.repositories.base_repo import BaseRepo


class BookRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(Book, books)
