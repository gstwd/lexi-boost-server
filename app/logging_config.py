import logging
import logging.handlers
import os


def setup_logging(app):
    if not app.debug:
        # Production logging
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # Main application log
        file_handler = logging.handlers.RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # Error log
        error_handler = logging.handlers.RotatingFileHandler(
            'logs/error.log',
            maxBytes=10240000,
            backupCount=5
        )
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        error_handler.setLevel(logging.ERROR)
        app.logger.addHandler(error_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

    else:
        # Development logging - console only
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(logging.DEBUG)

def log_request_info(app):
    @app.before_request
    def before_request():
        from flask import request
        app.logger.info(f'Request: {request.method} {request.url} - IP: {request.remote_addr}')

    @app.after_request
    def after_request(response):
        app.logger.info(f'Response: {response.status_code}')
        return response