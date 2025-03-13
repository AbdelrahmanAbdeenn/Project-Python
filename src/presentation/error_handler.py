from flask import jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

# def register_error_handlers(app):
    
#     @app.errorhandler(NotFound)
#     def handle_not_found(error):
#         return jsonify({"error": "Resource not found", "message": str(error)}), 404

#     @app.errorhandler(BadRequest)
#     def handle_bad_request(error):
#         return jsonify({"error": "Bad request", "message": str(error)}), 400

#     @app.errorhandler(IntegrityError)
#     def handle_integrity_error(error):
#         return jsonify({"error": "Duplicate entry, entity already exists"}), 400

#     @app.errorhandler(InternalServerError)
#     def handle_internal_server_error(error):
#         return jsonify({"error": "Internal server error", "message": str(error)}), 500

#     @app.errorhandler(Exception)
#     def handle_generic_error(error):
#         return jsonify({"error": "An unexpected error occurred", "message": str(error)}), 500



def register_error_handlers(app):
    
    @app.errorhandler(ValueError)
    def handle_value_error(error) -> jsonify:
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error) -> jsonify:
        return jsonify({"error": "Duplicate entry, entity already exists"}), 400

    @app.errorhandler(400)
    def bad_request_error(error) -> jsonify:
        return jsonify({"error": "Bad request, check input data"}), 400

    @app.errorhandler(404)
    def not_found_error(error) -> jsonify:
        return jsonify({"error": "Resource not found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error) -> jsonify:
        return jsonify({"error": "Internal server error, something went wrong!"}), 500

    @app.errorhandler(Exception)
    def handle_generic_error(error) -> jsonify:
        return jsonify({"error": "An unexpected error occurred!", "message": str(error)}), 500
