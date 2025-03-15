from flask import Flask

from src.presentation.book_api import BookApi
from src.presentation.borrow_api import BorrowAPI
from src.presentation.error_handling.error_handler import register_error_handlers
from src.presentation.member_api import MemberApi
from src.presentation.return_api import ReturnAPI

app = Flask("__name__")

if __name__ == "__main__":
    book_api = BookApi.as_view('book_api')
    member_api = MemberApi.as_view('member_api')
    borrow_api= BorrowAPI.as_view('borrow_api')
    return_api= ReturnAPI.as_view('return_api')
    app.add_url_rule('/book', view_func=book_api, methods=['GET', 'POST'])
    app.add_url_rule('/book/<int:id>', view_func=book_api, methods=['GET', 'PUT', 'DELETE'])
    app.add_url_rule('/member', view_func=member_api, methods=['GET', 'POST'])
    app.add_url_rule('/member/<int:id>', view_func=member_api, methods=['GET', 'PUT', 'DELETE'])
    app.add_url_rule('/borrow/<int:book_id>/<int:member_id>', view_func=borrow_api, methods=['POST'])
    app.add_url_rule('/return/<int:book_id>', view_func=return_api, methods=['POST'])
    
    register_error_handlers(app)
    app.run(debug=True)