from flask import Flask
from app.extensions import db, migrate
from app.error_handlers import register_error_handlers
from app.logging_config import setup_logging, log_request_info
from config import config
from app.data.repositories import WordRepository, StudyRecordRepository
from app.business.services import WordService, StudyService
from app.presentation.controllers import WordController, StudyController
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

    # Import models to ensure they are registered with SQLAlchemy
    from app.data import models

    # Dependency injection and route registration
    with app.app_context():
        # Create repository instances
        word_repository = WordRepository()
        study_record_repository = StudyRecordRepository()

        # Create service instances
        word_service = WordService(word_repository)
        study_service = StudyService(word_repository, study_record_repository)

        # Create controller instances and register blueprints
        word_controller = WordController(word_service)
        study_controller = StudyController(study_service)

        app.register_blueprint(word_controller.blueprint, url_prefix='/api')
        app.register_blueprint(study_controller.blueprint, url_prefix='/api')

    # Register API documentation
    from app.api_docs import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app