# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django REST API template project with a custom User model, token authentication, Docker setup, pytest testing, structured logging, and Swagger documentation. Built with Django 4.2 LTS (the latest long-term support version), the project uses PostgreSQL as the database and is optimized for production deployment with Gunicorn.

## Project Structure

```
.
├── backend/                      # Main Django application
│   ├── config/                   # Django project settings
│   │   ├── settings/
│   │   │   ├── base.py          # Base settings
│   │   │   └── local.py         # Local development settings
│   │   ├── urls.py              # Root URL configuration
│   │   └── wsgi.py              # WSGI configuration
│   ├── core/                     # Core application
│   │   ├── api/                 # REST API implementation
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── management/commands/ # Custom Django commands
│   │   ├── migrations/
│   │   ├── tests/               # Test suite
│   │   ├── admin.py
│   │   ├── factories.py         # Factory Boy factories
│   │   └── models.py            # Custom User model
│   ├── utils/                    # Shared utilities
│   │   └── logging/             # Structured logging configuration
│   │       ├── formatters.py    # Custom log formatters
│   │       ├── gconfig.py       # Gunicorn logging config
│   │       ├── loggers.py       # Logger setup
│   │       └── metadata.py      # Log metadata
│   └── manage.py
├── docker/
│   └── backend/
│       ├── Dockerfile           # Multi-stage Docker build
│       └── entrypoint.sh        # Entrypoint with multiple modes
├── docker-compose.yml           # Local development orchestration
├── pytest.ini                   # Pytest configuration
└── requirements.txt             # Python dependencies
```

## Environment Setup

The project uses Docker Compose for local development. The Django application runs in the `backend` service on port 8000.

**Environment variables** (configured via `.env` file, see `.env.example`):
- `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` - Database credentials
- `DEBUG` - Django debug mode (True for local development)
- `DJANGO_SETTINGS_MODULE` - Settings module (config.settings.local for dev)
- `NUMBER_OF_WORKERS` - Gunicorn worker count (default: 3)
- `WORKERS_TIMEOUT` - Gunicorn timeout (default: 290)
- `ADMIN_ENABLED`, `API_ENABLED` - Feature flags

## Common Commands

```bash
# Build containers
docker compose build

# Start services (runs on http://localhost:8000)
docker compose up

# Run tests with pytest (recommended)
docker compose run --rm --remove-orphans backend sh -c 'pytest'

# Run tests with coverage report
docker compose run --remove-orphans backend sh -c 'pytest --cov'

# Run project linting
docker compose run --remove-orphans backend sh -c 'flake8'

# Create superuser
docker compose run --remove-orphans backend sh -c 'python manage.py createsuperuser'

# Run migrations
docker compose run --remove-orphans backend sh -c 'python manage.py migrate'

# Create migrations
docker compose run --remove-orphans backend sh -c 'python manage.py makemigrations'

# Access Django shell
docker compose run --remove-orphans backend sh -c 'python manage.py shell'

# Access container shell
docker compose run backend sh
```

## Architecture

### Docker Configuration

**Multi-stage Dockerfile** (`docker/backend/Dockerfile`):
- **Base stage**: Python 3.9 slim with environment variables
- **Builder stage**: Installs dependencies using `uv` (ultra-fast package installer)
- **Runtime stage**: Minimal image with only runtime dependencies

**Entrypoint modes** (`docker/backend/entrypoint.sh`):
- Default (no command): Starts Gunicorn server for production
- `django`: Starts Django development server with auto-reload
- `ddtrace-gunicorn`: Starts Gunicorn with DataDog tracing
- Custom command: Pass any command to execute

The entrypoint automatically:
1. Waits for database (using `wait-for-it`)
2. Runs migrations
3. Starts the appropriate server

### Settings Structure
Split settings configuration for different environments:
- `backend/config/settings/base.py`: Base settings shared across environments
- `backend/config/settings/local.py`: Local development overrides (DEBUG=True)
- Control via `DJANGO_SETTINGS_MODULE` environment variable

### Custom User Model
Custom User model (`backend/core/models.py`) authenticating with email:
- Uses UUID as primary key (not auto-incrementing integers)
- Fields: `id` (UUID), `email` (unique), `name`, `is_active`, `is_staff`
- Custom `UserManager` handles user creation
- Set as `AUTH_USER_MODEL = 'core.User'` in settings

### API Structure
API endpoints organized by app in `backend/<app_name>/api/`:
- `serializers.py`: DRF serializers for request/response validation
- `views.py`: API views using DRF generics
- `urls.py`: URL routing with `app_name` namespace

**Current endpoints** (under `/api/core/`):
- `POST /api/core/create/`: Create new user
- `POST /api/core/token/`: Get authentication token
- `GET/PUT/PATCH /api/core/me/`: Manage authenticated user (requires token auth)

### Authentication
Token-based authentication using Django REST Framework:
- Tokens generated via email/password credentials
- Protected endpoints require `Authorization: Token <token>` header
- Swagger UI configured with Bearer token support

### Structured Logging
Custom logging infrastructure in `backend/utils/logging/`:
- **formatters.py**: JSON log formatters for structured logging
- **loggers.py**: Logger configuration and setup
- **gconfig.py**: Gunicorn-specific logging configuration
- **metadata.py**: Request metadata extraction for logs
- Uses `python-json-logger` for structured JSON output
- Integration with Gunicorn for access/error logging

### Testing Infrastructure
- Tests located in `backend/<app_name>/tests/`
- **pytest** is the recommended test runner (configured in `pytest.ini`)
  - Configuration uses `--reuse-db` and `--nomigrations` for faster tests
  - Automatically discovers tests matching `test_*.py` or `*_tests.py`
  - `DJANGO_SETTINGS_MODULE` set to `config.settings.local`
  - Test path: `backend/`
- Factory Boy used for test data generation (see `backend/core/factories.py`)
- Django's built-in test runner also available: `python manage.py test`
- Code quality enforced with flake8
- **Note**: When using pytest in Docker, use `--entrypoint=""` to bypass the migration entrypoint script

### API Documentation
Swagger/OpenAPI documentation configured with drf-yasg:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- JSON schema: http://localhost:8000/swagger.json
- Bearer token authentication support for protected endpoints

### Management Commands
Custom commands in `backend/core/management/commands/`:
- `wait_for_db`: Waits for PostgreSQL to be ready (legacy, replaced by wait-for-it)
- `populate_mock_data`: Creates test users (admin@test.com, user@test.com)

## Adding New Features

### Creating a New App
1. Create app directory under `backend/`
2. Add app to `INSTALLED_APPS` in `backend/config/settings/base.py`
3. Create `api/` subdirectory with `serializers.py`, `views.py`, and `urls.py`
4. Include app URLs in `backend/config/urls.py`
5. Create corresponding test directory structure: `<app>/tests/api/`

### Adding API Endpoints
1. Define serializers in `backend/<app>/api/serializers.py`
2. Create views in `backend/<app>/api/views.py` (use DRF generics/viewsets)
3. Wire up URLs in `backend/<app>/api/urls.py` with `app_name`
4. Add comprehensive tests in `backend/<app>/tests/api/`
5. Update Swagger documentation if needed

### Database Changes
1. Modify models in `backend/<app>/models.py`
2. Create migrations: `docker-compose run backend sh -c 'python manage.py makemigrations'`
3. Review generated migration files carefully
4. Apply migrations: `docker-compose run backend sh -c 'python manage.py migrate'`
5. Test migration rollback if needed

### Testing
Write tests following the existing structure:
- Test files should mirror source structure in `tests/` directory
- Use `UserFactory` (or create new factories in `factories.py`) for test data
- **Recommended**: Use pytest for running tests
  - Run all tests: `pytest` (inside container)
  - Run specific test file: `pytest core/tests/api/test_user.py`
  - Run specific test class: `pytest core/tests/api/test_user.py::PublicUserApiTest`
  - Run specific test function: `pytest core/tests/api/test_user.py::PublicUserApiTest::test_create_valid_user_success`
  - Run with coverage: `pytest --cov`
  - Run with verbose output: `pytest -v`
- Alternative: Django test runner: `python manage.py test <app>.tests.<module>`
- All tests must pass along with flake8 before committing
- Aim for high test coverage on new features

## Development Workflow

### Local Development
1. Make code changes in `backend/` directory (changes reflect immediately via volume mount)
2. Django dev server auto-reloads on file changes (when using `command: ["django"]`)
3. Run tests frequently to catch issues early
4. Use `flake8` to maintain code quality

### Docker Tips
- The `backend/` directory is mounted as a volume for live code reloading
- Database data persists in Docker volumes between restarts
- To reset database: `docker-compose down -v` (removes volumes)
- Use `--entrypoint=""` to bypass the automatic migration/server startup when running one-off commands

### Debugging
- Use `docker-compose logs backend` to view application logs
- Use `docker-compose logs db` to view database logs
- Access Python debugger: add `import pdb; pdb.set_trace()` in code
- For interactive debugging, ensure `stdin_open: true` and `tty: true` in docker-compose.yml

## Key Dependencies

- **Django 4.2 LTS**: Web framework (latest LTS version)
- **Django REST Framework 3.15**: API toolkit
- **psycopg2**: PostgreSQL adapter
- **pytest 8**: Testing framework
- **pytest-django**: Django integration for pytest
- **pytest-cov**: Coverage reporting
- **factory_boy**: Test fixture generation
- **drf-yasg**: Swagger/OpenAPI documentation
- **gunicorn 23**: WSGI HTTP server for production
- **python-json-logger 4**: Structured JSON logging
- **wait-for-it**: Database readiness checking

## Production Deployment Notes

- Uses Gunicorn as WSGI server (configured via entrypoint.sh)
- Structured JSON logging for log aggregation systems
- Multi-stage Docker build for smaller image size
- Configurable worker count and timeout via environment variables
- Optional DataDog APM tracing support (`ddtrace-gunicorn` mode)
- Static files should be served via reverse proxy (Nginx recommended)
