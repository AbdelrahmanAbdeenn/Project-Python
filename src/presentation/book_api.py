from flask.views import MethodView
from src.application.book_services import BookServices
from typing import Optional, Any, List
from src.domain.entities import Book
from flask import request , jsonify

class BookApi(MethodView):
    def __init__(self) -> None:
        self.bookServices = BookServices()

    def get(self, id: Optional[int] = None) -> Book | List[Book]:
        return self.bookServices.get(id)
    
    def post(self) -> Book:
        data = request.get_json()
        if not data.get("title") or not data.get("author"):
            raise ValueError("Title and author are required")
        return self.bookServices.create(data)
    
    def put(self, id) -> Book:
        data = request.get_json()
        if "book_id" in data and data['book_id']!=id:
            raise ValueError("Updating book_id is not allowed")
        return self.bookServices.update(id, data)

    def delete(self, id: int) -> str:
        return self.bookServices.delete(id)
    
