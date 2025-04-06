from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.presentation.error_handling.error_handler import register_error_handlers
from src.presentation.middleware.auth_middleware import AuthMiddleware
from src.presentation.routes.book_api import router as bookRouter
from src.presentation.routes.borrow_api import router as borrowRouter
from src.presentation.routes.member_api import router as memberRouter
from src.presentation.routes.return_api import router as returnRouter

app = FastAPI()
app.add_middleware(AuthMiddleware)


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(title='library management', version='0.0.1', routes=app.routes)

    openapi_schema['components'] = openapi_schema['components'] or {}
    openapi_schema['components']['securitySchemes'] = {'BearerAuth': {
        'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'}}
    openapi_schema['security'] = [{'BearerAuth': []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore


app.include_router(bookRouter)
app.include_router(memberRouter)
app.include_router(borrowRouter)
app.include_router(returnRouter)
register_error_handlers(app)
