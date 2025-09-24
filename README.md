# Lexi Boost Server

Flask-based backend API server for a vocabulary learning application. Built with **three-layer architecture** featuring comprehensive error handling, input validation, logging, testing, and API documentation.

## Features

- **Three-Layer Architecture** with proper separation of concerns
- **Repository Pattern** with interfaces for better testability
- **RESTful API** with Flask-RESTX for interactive documentation
- **Service Layer** with business logic encapsulation
- **BaseController Pattern** eliminates code duplication across controllers
- **Standardized Error Handling** with HTTP 200 + business error codes for API consistency
- **Data Transfer Objects** for clean data flow
- **Database Management** with SQLAlchemy and Alembic migrations
- **Input Validation** using Marshmallow schemas
- **Comprehensive Logging** with rotating file logs
- **Global Error Handlers** with unified response format
- **Testing Framework** with pytest and full coverage
- **API Documentation** with Swagger/OpenAPI

## Architecture Overview

This project follows a **Three-Layer Architecture** pattern:

- **Presentation Layer** (`app/presentation/`): Controllers inherit from BaseController for consistency
- **Business Logic Layer** (`app/business/`): Services contain domain logic and business rules
- **Data Access Layer** (`app/data/`): Repositories manage database operations

This architecture provides better:
- **Separation of Concerns**: Each layer has distinct responsibilities
- **Testability**: Easy to unit test each layer independently
- **Maintainability**: Changes in one layer don't affect others
- **Scalability**: Easy to modify or extend functionality

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database

### Installation

1. Clone the repository and navigate to project directory
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure environment variables in `.env` file
6. Initialize database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### Running the Application

- Development server: `python run.py`
- Flask CLI: `flask run`
- Access API documentation: `http://localhost:5000/api/docs/`

### Testing

- Run all tests: `pytest`
- Run with coverage: `pytest --cov=app`
- Run specific test: `pytest tests/test_api.py`

## Development Workflow

### Adding New API Endpoints

1. **Design Data Model** (if needed)
   ```bash
   # Edit app/data/models/ to add new model
   flask db migrate -m "add new model"
   flask db upgrade
   ```

2. **Create Repository Interface and Implementation**
   - Add interface in `app/data/repositories/`
   - Implement concrete repository class
   - Define data access methods

3. **Define DTOs and Service**
   - Create DTO in `app/business/dto/`
   - Add service class in `app/business/services/`
   - Implement business logic

4. **Define Validation Schema**
   - Add marshmallow schema in `app/presentation/schemas/`
   - Define request/response validation rules

5. **Implement Controller**
   - Create controller in `app/presentation/controllers/`
   - Inherit from BaseController to eliminate boilerplate code
   - Handle HTTP requests and responses
   - Use dependency injection for services

6. **Register Dependencies**
   - Update `app/__init__.py` to register new components
   - Set up dependency injection

7. **Write Tests**
   - Add comprehensive tests in `tests/`
   - Test repositories, services, and controllers
   - Run tests: `pytest`

### Modifying Existing Endpoints

1. **Update Repository** (if needed)
   - Modify repository implementation in `app/data/repositories/`
   - Update interface if needed

2. **Update Service Logic**
   - Modify business logic in `app/business/services/`
   - Update DTOs if data structure changes

3. **Update Controller**
   - Modify controller in `app/presentation/controllers/`
   - Leverage BaseController for common functionality
   - Maintain backward compatibility when possible

4. **Update Validation Rules**
   - Modify schemas in `app/presentation/schemas/`
   - Ensure data integrity

5. **Database Changes** (if needed)
   ```bash
   flask db migrate -m "describe changes"
   flask db upgrade
   ```

6. **Update Tests**
   - Modify existing tests to reflect changes
   - Add new test cases for new functionality

### Managing Dependencies

1. **Adding New Dependencies**
   ```bash
   pip install package-name
   pip freeze > requirements.txt
   ```

2. **Configure Extensions**
   - Initialize in `app/extensions.py`
   - Register in `app/__init__.py`

3. **Update Documentation**
   - Document new features in README
   - Update API documentation if needed

## Development Guidelines

### Architecture Guidelines

- **Layer Separation**: Don't skip layers (e.g., controllers shouldn't call repositories directly)
- **Dependency Direction**: Higher layers depend on lower layers via interfaces
- **Single Responsibility**: Each class should have one reason to change
- **Interface Segregation**: Use specific interfaces rather than large general ones

### Code Standards

- **Error Handling**: Use custom exceptions from `app/exceptions.py`
- **Controller Pattern**: Inherit from BaseController for consistency and DRY principle
- **API Response Format**: ALL responses use HTTP 200 with business error codes following API design standards:
  ```json
  {
    "code": 0,
    "message": "success",
    "data": {...}
  }
  ```
- **Global Error Handling**: Controllers don't need try-catch blocks - use global handlers
- **Database Operations**: Always wrap in try-catch with rollback
- **Validation**: Use marshmallow schemas for all input validation
- **Logging**: Use configured loggers, avoid print statements

### Error Codes

**API Design Standard**: All responses use HTTP 200 with business error codes for frontend consistency.

- `0`: Success
- `1001`: Validation Error
- `1002`: Not Found
- `1003`: Database Error
- `1004`: Authentication Error
- `1005`: Authorization Error
- `1006`: Method Not Allowed
- `500`: Internal Server Error (system fallback)

### Testing Requirements

- Write tests for all new endpoints
- Maintain test coverage above 80%
- Use descriptive test names
- Test both success and failure scenarios
- Use test fixtures for consistent setup

### Database Migration Best Practices

- Always review generated migration files
- Test migrations on development data
- Use descriptive migration messages
- Never edit existing migration files
- Backup data before running migrations in production

## Project Structure

```
app/
   __init__.py                      # Flask app factory with dependency injection
   extensions.py                    # Flask extensions
   exceptions.py                    # Custom exceptions
   error_handlers.py               # Global error handlers
   logging_config.py               # Logging configuration
   api_docs.py                     # API documentation setup
   data/                           # Data Access Layer
      models/                      # Database models
         word.py                   # Word entity
         study_record.py           # StudyRecord entity
      repositories/                # Repository implementations
         word_repository.py        # Word data access
         study_record_repository.py # StudyRecord data access
   business/                       # Business Logic Layer
      dto/                         # Data Transfer Objects
         word_dto.py               # Word DTO
         study_record_dto.py       # StudyRecord DTO
      services/                    # Business services
         word_service.py           # Word business logic
         study_service.py          # Study business logic
   presentation/                   # Presentation Layer
      controllers/                 # HTTP controllers
         base_controller.py        # Abstract base controller with common functionality
         word_controller.py        # Word API endpoints
         study_controller.py       # Study API endpoints
      schemas/                     # Request/response validation
         validation_schemas.py     # Marshmallow schemas
tests/                             # Test suite
migrations/                        # Database migrations
logs/                              # Application logs
config.py                         # Configuration classes
run.py                            # Application entry point
requirements.txt                  # Dependencies
```

## API Endpoints

- `GET /api/words` - Retrieve all vocabulary words
- `POST /api/study` - Record study session result

## Environment Configuration

Create `.env` file with:
```
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lexi_boost
DB_USER=username
DB_PASSWORD=password

# Flask
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=your-secret-key
```

## Contributing

1. Follow the development workflow outlined above
2. Ensure all tests pass before committing
3. Use descriptive commit messages
4. Update documentation for new features
5. Follow existing code patterns and conventions