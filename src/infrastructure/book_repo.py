from src.infrastructure.base_repo import BaseRepo
from src.domain.entities import Book
from src.infrastructure.database.schema import books
from flask import jsonify

class BookRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(Book, books , 'book_id')
