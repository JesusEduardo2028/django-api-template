# Backend - CLAUDE.md

This file provides guidance to Claude Code when working with the Django backend.

## Architecture Overview

Django 4.2 LTS REST API with:
- Custom User model (UUID primary key, email authentication)
- Token-based authentication (Django REST Framework)
- PostgreSQL database
- Multi-stage Docker build
- Structured JSON logging
- Comprehensive test coverage with pytest

## Project Structure

```
backend/
├── config/                   # Django project configuration
│   ├── settings/
│   │   ├── base.py          # Shared settings, CORS config
│   │   └── local.py         # Development overrides
│   ├── urls.py              # Root URL routing (includes Swagger)
│   └── wsgi.py              # WSGI application
├── core/                     # Core application
│   ├── api/                 # REST API layer
│   │   ├── serializers.py  # User serializers
│   │   ├── views.py        # User API views
│   │   └── urls.py         # API URL patterns
│   ├── management/commands/
│   │   ├── wait_for_db.py  # Database readiness check
│   │   └── populate_mock_data.py # Test data generation
│   ├── migrations/          # Database migrations
│   ├── tests/              # Test suite
│   │   ├── api/
│   │   │   └── test_user.py # User API tests
│   │   └── test_models.py  # Model tests
│   ├── admin.py            # Django admin customization
│   ├── factories.py        # Factory Boy test factories
│   └── models.py           # Custom User model
├── utils/                    # Shared utilities
│   └── logging/             # Structured logging infrastructure
│       ├── formatters.py   # JSON log formatter
│       ├── gconfig.py      # Gunicorn logging config
│       ├── loggers.py      # Logger configuration
│       └── metadata.py     # Request metadata
└── manage.py                # Django management script
```

## Key Files

### Settings (config/settings/)

**base.py** (line 175-177):
- CORS configuration for frontend integration
- Middleware includes `corsheaders.middleware.CorsMiddleware` (line 85)
- Custom User model: `AUTH_USER_MODEL = 'core.User'` (line 172)
- Installed apps include `rest_framework`, `corsheaders`, `drf_yasg`

**local.py**:
- Inherits from base.py
- Sets DEBUG=True for development
- Development-specific overrides

### Models (core/models.py)

**User Model**:
- UUID primary key: `id = models.UUIDField(primary_key=True, default=uuid.uuid4)`
- Email authentication: `USERNAME_FIELD = 'email'`
- Custom UserManager for user creation
- Fields: email (unique), name, is_active, is_staff, is_superuser

### API Layer (core/api/)

**serializers.py**:
- `UserSerializer`: User representation
- `AuthTokenSerializer`: Login validation
- Uses `gettext_lazy` for translations (not deprecated `ugettext_lazy`)

**views.py**:
- `CreateUserView`: User registration (no auth required)
- `CreateTokenView`: Token generation (no auth required)
- `ManageUserView`: Get/update current user (requires authentication)

**urls.py**:
- URL patterns with `app_name = 'user'` namespace
- Endpoints: `create/`, `token/`, `me/`

### Testing (core/tests/)

**Configuration**:
- pytest configured in project root `pytest.ini`
- Test path: `testpaths = backend`
- Settings: `DJANGO_SETTINGS_MODULE = config.settings.local`
- Uses `--reuse-db` and `--nomigrations` for speed

**test_user.py**:
- `PublicUserApiTest`: Unauthenticated endpoints
- `PrivateUserApiTest`: Authenticated endpoints
- Uses `UserFactory` for test data

**factories.py**:
- `UserFactory`: Generates test users with Factory Boy
- Handles password hashing correctly

## Common Commands

All commands from project root:

```bash
# Testing
docker compose run --rm backend sh -c 'pytest'
docker compose run --rm backend sh -c 'pytest --cov'
docker compose run --rm backend sh -c 'pytest -v'
docker compose run --rm backend sh -c 'flake8'

# Migrations
docker compose run --rm backend sh -c 'python manage.py makemigrations'
docker compose run --rm backend sh -c 'python manage.py migrate'

# User management
docker compose run --rm backend sh -c 'python manage.py createsuperuser'
docker compose run --rm backend sh -c 'python manage.py populate_mock_data'

# Shell access
docker compose run --rm backend sh -c 'python manage.py shell'
docker compose run backend sh
```

## Development Workflow

### Adding New API Endpoints

1. **Create/update serializers** in `backend/core/api/serializers.py`
   - Use DRF serializers for validation
   - Add field validation in `validate_<field>()` methods

2. **Create views** in `backend/core/api/views.py`
   - Use DRF generics (CreateAPIView, RetrieveUpdateAPIView, etc.)
   - Set `authentication_classes` for protected endpoints
   - Set `permission_classes` (IsAuthenticated, AllowAny)

3. **Wire up URLs** in `backend/core/api/urls.py`
   - Add to `urlpatterns` with descriptive names

4. **Write tests** in `backend/core/tests/api/`
   - Test both authenticated and unauthenticated scenarios
   - Use `UserFactory` for test data
   - Test validation, permissions, edge cases

### Database Changes

1. **Modify models** in `backend/core/models.py`
   - Follow Django model best practices
   - Add indexes for frequently queried fields

2. **Generate migrations**:
   ```bash
   docker compose run --rm backend sh -c 'python manage.py makemigrations'
   ```

3. **Review migration files** carefully before applying

4. **Apply migrations**:
   ```bash
   docker compose run --rm backend sh -c 'python manage.py migrate'
   ```

### Creating New Django Apps

1. Create directory under `backend/`
2. Add to `INSTALLED_APPS` in `config/settings/base.py`
3. Create `api/` subdirectory with standard files
4. Create `tests/` directory
5. Wire up URLs in `config/urls.py`

## Important Notes

### Authentication

- Token authentication using DRF's `rest_framework.authtoken`
- Tokens generated via `/api/core/token/` endpoint
- Protected endpoints require header: `Authorization: Token <token>`
- Swagger UI has Bearer token support configured

### CORS Configuration

- CORS middleware positioned correctly (before CommonMiddleware)
- Location: `config/settings/base.py:85`
- Allows frontend on `http://localhost:3000`
- `CORS_ALLOW_CREDENTIALS = True` for token support

### Testing Best Practices

- Always write tests for new API endpoints
- Use pytest (not Django's test runner) for consistency
- Aim for >90% code coverage
- Test authentication, permissions, validation
- Use factories for test data (don't create manually)
- Run `flake8` before committing

### Deprecated Imports (FIXED)

- Use `django.utils.translation.gettext_lazy` (not `ugettext_lazy`)
- Use `from pythonjsonlogger import json as jsonlogger` (correct import path)
- Don't set `USE_L10N` in settings (deprecated in Django 4.0+)

## Docker Configuration

**Dockerfile** (`../docker/backend/Dockerfile`):
- Multi-stage build (base → builder → runtime)
- Uses `uv` for fast dependency installation
- Python 3.9-slim-bookworm base image

**Entrypoint** (`../docker/backend/entrypoint.sh`):
- Waits for database with `wait-for-it`
- Runs migrations automatically
- Modes: `django` (dev server), `ddtrace-gunicorn` (prod with APM), default (gunicorn)

## Logging

Structured JSON logging configured in `backend/utils/logging/`:
- All logs output as JSON for log aggregation
- Request metadata automatically included
- Gunicorn access/error logs use JSON format
- Production-ready for centralized logging systems

## Swagger Documentation

- UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Configured in `config/urls.py`
- Bearer token authentication support
- Setting: `SWAGGER_USE_COMPAT_RENDERERS = False` (config/settings/base.py:186)

## Key Dependencies

- Django 4.2.27 (LTS)
- djangorestframework 3.15.2
- psycopg2-binary 2.9.10
- pytest 8.4.2
- pytest-django 4.9.0
- factory_boy 3.3.1
- drf-yasg 1.21.11
- gunicorn 23.0.0
- python-json-logger 4.0.0

## Common Issues

### Migrations Not Applied
Run: `docker compose run --rm backend sh -c 'python manage.py migrate'`

### Test Database Issues
pytest uses `--reuse-db` for speed. If schema changes, run: `pytest --create-db`

### CORS Errors from Frontend
Check `CORS_ORIGIN_WHITELIST` in `config/settings/base.py:175`
Ensure `corsheaders.middleware.CorsMiddleware` is in MIDDLEWARE

### Import Errors
Make sure you're in the backend directory context when running management commands
