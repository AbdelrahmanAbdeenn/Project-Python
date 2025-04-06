from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if (request.url.path == "/docs" or request.url.path == "/openapi.json"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                {"detail": "Missing Authorization header"},
                status_code=401
            )

        token = auth_header.replace("Bearer ", "")

        if token != "secret-token":
            return JSONResponse(
                {"detail": "Invalid or expired token"},
                status_code=401
            )

        response = await call_next(request)
        return response
