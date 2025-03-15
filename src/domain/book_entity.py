from datetime import datetime
from typing import Optional

from src.domain.base_entity import BaseEntity


class Book(BaseEntity):
    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        is_borrowed: bool,
        borrowed_date: Optional[datetime] = None,
        borrowed_by: Optional[int] = None,
    ) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        self.borrowed_date = borrowed_date
        self.borrowed_by = borrowed_by
