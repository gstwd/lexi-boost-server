from flask import jsonify

from app.exceptions import APIException


def register_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = {
            'code': error.error_code,
            'message': error.message,
            'data': None
        }
        return jsonify(response), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        response = {
            'code': 1002,
            'message': 'Resource not found',
            'data': None
        }
        return jsonify(response), 404

    @app.errorhandler(500)
    def handle_internal_error(error):
        app.logger.error(f'Internal server error: {error}')
        response = {
            'code': 1003,
            'message': 'Internal server error',
            'data': None
        }
        return jsonify(response), 500

    @app.errorhandler(400)
    def handle_bad_request(error):
        response = {
            'code': 1001,
            'message': 'Bad request',
            'data': None
        }
        return jsonify(response), 400

    @app.errorhandler(401)
    def handle_unauthorized(error):
        response = {
            'code': 1004,
            'message': 'Unauthorized',
            'data': None
        }
        return jsonify(response), 401

    @app.errorhandler(403)
    def handle_forbidden(error):
        response = {
            'code': 1005,
            'message': 'Forbidden',
            'data': None
        }
        return jsonify(response), 403

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        response = {
            'code': 1006,
            'message': 'Method not allowed',
            'data': None
        }
        return jsonify(response), 405