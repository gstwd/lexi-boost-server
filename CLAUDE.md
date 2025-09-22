# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based backend API server for a vocabulary learning application (Lexi Boost). The project uses PostgreSQL as the database and follows a modular Flask application structure with comprehensive error handling, validation, logging, testing, and API documentation.

## Project Structure

```
├── app/
│   ├── __init__.py          # Flask app factory with all integrations
│   ├── extensions.py        # Flask extensions (SQLAlchemy, Migrate)
│   ├── models.py           # Database models (Word, StudyRecord)
│   ├── exceptions.py       # Custom exception classes
│   ├── error_handlers.py   # Global error handlers
│   ├── validators.py       # Input validation with marshmallow
│   ├── logging_config.py   # Logging configuration
│   ├── api_docs.py         # API documentation with Flask-RESTX
│   └── routes/
│       ├── __init__.py     # Route registration
│       └── words.py        # API endpoints with validation
├── tests/
│   ├── conftest.py         # Pytest configuration and fixtures
│   ├── test_api.py         # API endpoint tests
│   └── test_models.py      # Database model tests
├── logs/                   # Application logs (created automatically)
├── migrations/             # Database migration files
├── config.py              # Configuration classes (dev/prod/test)
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
└── .env                   # Environment variables (not in git)

```

## Key Features

### 1. Error Handling
- Custom exception classes for different error types
- Global error handlers for consistent JSON responses
- Automatic error logging

### 2. Input Validation
- Marshmallow schemas for request validation
- Decorators for automatic validation
- Comprehensive error messages

### 3. Logging System
- Rotating file logs for production
- Console logging for development
- Request/response logging
- Separate error logs

### 4. Testing Framework
- Pytest with Flask integration
- Comprehensive test coverage
- Test database configuration
- API and model tests

### 5. API Documentation
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

- Use custom exceptions instead of generic Exception
- All API endpoints use input validation
- Database operations are wrapped in try-catch with rollback
- Logging is automatically configured based on environment
- Tests use in-memory SQLite for speed