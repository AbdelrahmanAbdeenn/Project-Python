from fastapi import FastAPI
from src.presentation.book_api import router as bookRouter
from src.presentation.borrow_api import router as borrowRouter
from src.presentation.error_handling.error_handler import register_error_handlers
from src.presentation.member_api import router as memberRouter
from src.presentation.return_api import router as returnRouter

app = FastAPI()
app.include_router(bookRouter)
app.include_router(memberRouter)
app.include_router(borrowRouter)
app.include_router(returnRouter)
register_error_handlers(app)
# register_error_handlers(app)
# app.run(debug=True)
