from flask.views import MethodView

from src.application.book_services import BookServices


class BorrowAPI(MethodView):
    def __init__(self) -> None:
        self.bookServices = BookServices()

    def post(self, book_id: int, member_id: int) -> dict[str, str]:
        return self.bookServices.borrow_book(book_id, member_id)
