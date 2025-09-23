# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based backend API server for a vocabulary learning application (Lexi Boost). The project uses PostgreSQL as the database and follows a three-layer architecture pattern with comprehensive error handling, validation, logging, testing, and API documentation.

## Architecture Overview

The project follows a **Three-Layer Architecture** pattern that separates concerns into distinct layers:

1. **Presentation Layer** (`app/presentation/`): Handles HTTP requests/responses, input validation, and user interface concerns
2. **Business Logic Layer** (`app/business/`): Contains domain logic, business rules, and service operations
3. **Data Access Layer** (`app/data/`): Manages database operations, models, and data persistence

This architecture provides better maintainability, testability, and separation of concerns compared to a simple MVC pattern.

## Project Structure

```
├── app/
│   ├── __init__.py                      # Flask app factory with dependency injection
│   ├── extensions.py                    # Flask extensions (SQLAlchemy, Migrate)
│   ├── exceptions.py                    # Custom exception classes
│   ├── error_handlers.py               # Global error handlers
│   ├── logging_config.py               # Logging configuration
│   ├── api_docs.py                     # API documentation with Flask-RESTX
│   ├── data/                           # Data Access Layer
│   │   ├── __init__.py
│   │   ├── models/                     # Database models
│   │   │   ├── __init__.py
│   │   │   ├── word.py                 # Word model
│   │   │   └── study_record.py         # StudyRecord model
│   │   └── repositories/               # Repository pattern implementations
│   │       ├── __init__.py
│   │       ├── word_repository_interface.py
│   │       ├── word_repository.py
│   │       ├── study_record_repository_interface.py
│   │       └── study_record_repository.py
│   ├── business/                       # Business Logic Layer
│   │   ├── dto/                        # Data Transfer Objects
│   │   │   ├── __init__.py
│   │   │   ├── word_dto.py
│   │   │   └── study_record_dto.py
│   │   └── services/                   # Business logic services
│   │       ├── __init__.py
│   │       ├── word_service.py
│   │       └── study_service.py
│   └── presentation/                   # Presentation Layer
│       ├── controllers/                # HTTP controllers
│       │   ├── __init__.py
│       │   ├── word_controller.py
│       │   └── study_controller.py
│       └── schemas/                    # Request/response validation schemas
│           ├── __init__.py
│           └── validation_schemas.py
├── tests/
│   ├── conftest.py                     # Pytest configuration and fixtures
│   ├── test_api.py                     # API endpoint tests
│   └── test_models.py                  # Database model tests
├── logs/                               # Application logs (created automatically)
├── migrations/                         # Database migration files
├── config.py                          # Configuration classes (dev/prod/test)
├── run.py                             # Application entry point
├── requirements.txt                   # Python dependencies
├── pytest.ini                        # Pytest configuration
└── .env                               # Environment variables (not in git)

```

## Key Features

### 1. Error Handling
- Custom exception classes for different error types
- Global error handlers for consistent JSON responses
- Automatic error logging

### 2. Three-Layer Architecture
- **Repository Pattern**: Abstracts data access with interfaces
- **Service Layer**: Contains business logic and domain operations
- **Controller Layer**: Handles HTTP requests and responses
- **Dependency Injection**: Proper IoC container for loose coupling
- **DTOs**: Data Transfer Objects for clean data flow between layers

### 3. Input Validation
- Marshmallow schemas for request validation
- Decorators for automatic validation
- Comprehensive error messages

### 4. Logging System
- Rotating file logs for production
- Console logging for development
- Request/response logging
- Separate error logs

### 5. Testing Framework
- Pytest with Flask integration
- Comprehensive test coverage
- Test database configuration
- API and model tests

### 6. API Documentation
- Swagger/OpenAPI documentation with Flask-RESTX
- Interactive API docs at `/api/docs/`
- Request/response models

## Setup Commands

1. Create virtual environment: `python -m venv venv`
2. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
3. Install dependencies: `pip install -r requirements.txt`
4. Configure database in `.env` file
5. Initialize database: `flask db init` (if migrations folder doesn't exist)
6. Create migration: `flask db migrate -m "Initial migration"`
7. Apply migration: `flask db upgrade`

## Running the Application

- Development server: `python run.py`
- Flask CLI: `flask run`
- The server runs on `http://localhost:5000`
- API documentation: `http://localhost:5000/api/docs/`

## Testing

- Run all tests: `pytest`
- Run with coverage: `pytest --cov=app`
- Run specific test file: `pytest tests/test_api.py`
- Run with verbose output: `pytest -v`

## API Endpoints

- `GET /api/words` - Get all words
- `POST /api/study` - Save study result (requires `word_id` and `status`)

All responses follow the format: `{"code": 0, "message": "success", "data": ...}`

## Error Codes

- 0: Success
- 1001: Validation Error
- 1002: Not Found
- 1003: Database Error
- 1004: Authentication Error
- 1005: Authorization Error
- 1006: Method Not Allowed

## Database Models

- **Word**: id, word, meaning, created_at
- **StudyRecord**: id, word_id, status, created_at, updated_at

## Environment Variables

Configure these in the `.env` file:
- DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
- FLASK_ENV, FLASK_DEBUG, SECRET_KEY

## Development Notes

- Follow three-layer architecture principles
- Use repository interfaces for testability and loose coupling
- Services contain business logic, not controllers
- Use DTOs for data transfer between layers
- Controllers handle only HTTP concerns (request/response)
- Use custom exceptions instead of generic Exception
- All API endpoints use input validation
- Database operations are wrapped in try-catch with rollback
- Logging is automatically configured based on environment
- Tests use in-memory SQLite for speed

## Layer Responsibilities

### Data Access Layer (`app/data/`)
- Database models (entities)
- Repository interfaces and implementations
- Data persistence logic
- Database migrations

### Business Logic Layer (`app/business/`)
- Domain services with business rules
- Data Transfer Objects (DTOs)
- Business logic validation
- Cross-cutting concerns

### Presentation Layer (`app/presentation/`)
- HTTP controllers
- Request/response handling
- Input validation schemas
- API routing and blueprints