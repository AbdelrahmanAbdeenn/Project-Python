from typing import Dict

from flask.views import MethodView

from src.application.book_services import BookServices


class ReturnAPI(MethodView):
    def __init__(self) -> None:
        self.bookServices = BookServices()

    def post(self, book_id: int) -> Dict[str, str]:
        return self.bookServices.return_book(book_id)
