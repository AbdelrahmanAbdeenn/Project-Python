from dataclasses import dataclass
from datetime import datetime

from src.domain.base_entity import BaseEntity


@dataclass
class Book(BaseEntity):
    title: str
    author: str
    is_borrowed: bool
    borrowed_date: datetime | None = None
    borrowed_by: int | None = None
    id: int | None = None
