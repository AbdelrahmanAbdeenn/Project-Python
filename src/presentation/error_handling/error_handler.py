from flask import Flask, Response, jsonify
from sqlalchemy.exc import IntegrityError


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError) -> tuple[Response, int]:
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error: IntegrityError) -> tuple[Response, int]:
        return jsonify({"error": "Duplicate entry, entity already exists"}), 400

    @app.errorhandler(400)
    def bad_request_error(error: Exception) -> tuple[Response, int]:
        return jsonify({"error": "Bad request, check input data"}), 400

    @app.errorhandler(404)
    def not_found_error(error: Exception) -> tuple[Response, int]:
        return jsonify({"error": "Resource not found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error: Exception) -> tuple[Response, int]:
        return jsonify({"error": "Internal server error, something went wrong!"}), 500

    @app.errorhandler(Exception)
    def handle_generic_error(error: Exception) -> tuple[Response, int]:
        return jsonify({"error": "An unexpected error occurred!", "message": str(error)}), 500
