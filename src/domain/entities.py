from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class BaseEntity:
    def __init__(self) -> None:
        pass

class Book(BaseEntity):
    book_id: int
    title: str
    author: str
    is_borrowed: bool
    borrowed_date: Optional[datetime]= None
    borrowed_by: Optional[int] = None
    
    def __init__(self, book_id: int, title: str, author: str, is_borrowed: bool, borrowed_date: Optional[datetime] = None, borrowed_by: Optional[int] = None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        self.borrowed_date = borrowed_date
        self.borrowed_by = borrowed_by
    
class Member(BaseEntity):
    member_id: int
    name: str
    email: str
    def __init__(self, name: str, email: str, member_id: int):
        self.member_id = member_id
        self.name = name
        self.email = email