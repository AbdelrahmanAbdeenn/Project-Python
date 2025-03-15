from typing import Optional

from flask import Response, jsonify, request
from flask.views import MethodView

from src.application.book_services import BookServices


class BookApi(MethodView):
    def __init__(self) -> None:
        self.book_services = BookServices()

    def get(self, id: Optional[int] = None) -> Response:
        book = self.book_services.get(id)

        if isinstance(book, list):
            return jsonify([vars(b) for b in book])
        return jsonify(vars(book))

    def post(self) -> Response:
        data = request.get_json()
        if not data.get("title") or not data.get("author"):
            raise ValueError("Title and Author are required")

        book = self.book_services.create(data)
        return jsonify(vars(book))

    def put(self, id: int) -> Response:
        data = request.get_json()
        book = self.book_services.update(id, data)
        return jsonify(vars(book))

    def delete(self, id: int) -> Response:
        return jsonify(self.book_services.delete(id))
