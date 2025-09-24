from flask import jsonify

from app.exceptions import APIException


def register_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        """Handle business exceptions with HTTP 200 and business error codes"""
        response = {
            'code': error.error_code,
            'message': error.message,
            'data': None
        }
        return jsonify(response), 200

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handle all other exceptions as internal server errors"""
        app.logger.error(f'Unhandled exception: {error}')
        response = {
            'code': 500,
            'message': 'Internal server error',
            'data': None
        }
        return jsonify(response), 200

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle Flask 404 errors"""
        response = {
            'code': 1002,
            'message': 'Resource not found',
            'data': None
        }
        return jsonify(response), 200

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle Flask 405 errors"""
        response = {
            'code': 1006,
            'message': 'Method not allowed',
            'data': None
        }
        return jsonify(response), 200