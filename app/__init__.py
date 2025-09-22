from flask import Flask
from app.extensions import db, migrate
from app.routes import register_routes
from app.error_handlers import register_error_handlers
from app.logging_config import setup_logging, log_request_info
from config import config
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register error handlers
    register_error_handlers(app)

    # Setup logging
    setup_logging(app)
    log_request_info(app)

    # Register routes
    register_routes(app)

    # Register API documentation
    from app.api_docs import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Import models to ensure they are registered with SQLAlchemy
    from app import models

    return app