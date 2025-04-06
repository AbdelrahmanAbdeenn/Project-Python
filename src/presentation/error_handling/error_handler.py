from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": str(exc)}
        )

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": "Duplicate entry, entity already exists"}
        )

    @app.exception_handler(400)
    async def bad_request_error(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": "Bad request, check input data"}
        )

    @app.exception_handler(404)
    async def not_found_error(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"error": "Resource not found", "message": str(exc)}
        )

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error, something went wrong!"}
        )

    @app.exception_handler(Exception)
    async def handle_generic_error(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred!", "message": str(exc)}
        )
