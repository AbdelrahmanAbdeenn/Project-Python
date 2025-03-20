from flask import Response, jsonify
from flask.views import MethodView

from src.application.book_services import BookServices


class ReturnAPI(MethodView):
    def __init__(self) -> None:
        self.bookServices = BookServices()

    def post(self, id: int) -> Response:
        return jsonify(self.bookServices.return_book(id))
