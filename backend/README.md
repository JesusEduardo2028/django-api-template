# Django REST API Backend

A Django 4.2 LTS REST API with custom User model, token authentication, and PostgreSQL.

## Quick Start

**From project root directory:**

```bash
# Build backend
docker compose build backend

# Start services (backend will run on http://localhost:8000)
docker compose up

# Run tests
docker compose run --rm backend sh -c 'pytest'

# Run tests with coverage
docker compose run --rm backend sh -c 'pytest --cov'
```

## API Documentation

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **JSON Schema**: http://localhost:8000/swagger.json

## Development Commands

### Database Migrations

```bash
# Create migrations
docker compose run --rm backend sh -c 'python manage.py makemigrations'

# Apply migrations
docker compose run --rm backend sh -c 'python manage.py migrate'
```

### User Management

```bash
# Create superuser
docker compose run --rm backend sh -c 'python manage.py createsuperuser'

# Populate mock data (creates admin@test.com and user@test.com)
docker compose run --rm backend sh -c 'python manage.py populate_mock_data'
```

### Django Shell

```bash
# Access Django shell
docker compose run --rm backend sh -c 'python manage.py shell'

# Access container shell
docker compose run backend sh
```

### Code Quality

```bash
# Run linting
docker compose run --rm backend sh -c 'flake8'
```

## Project Structure

```
backend/
├── config/                   # Django project settings
│   ├── settings/
│   │   ├── base.py          # Base settings
│   │   └── local.py         # Local development settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI configuration
├── core/                     # Core application
│   ├── api/                 # REST API implementation
│   │   ├── serializers.py  # DRF serializers
│   │   ├── views.py        # API views
│   │   └── urls.py         # API URL routing
│   ├── management/commands/ # Custom Django commands
│   ├── migrations/          # Database migrations
│   ├── tests/              # Test suite
│   ├── admin.py            # Django admin configuration
│   ├── factories.py        # Factory Boy factories
│   └── models.py           # Custom User model
├── utils/                    # Shared utilities
│   └── logging/             # Structured logging
└── manage.py                # Django management script
```

## Custom User Model

The project uses a custom User model with the following features:

- **Primary Key**: UUID (not auto-incrementing integer)
- **Authentication**: Email-based (not username)
- **Fields**: `id`, `email`, `name`, `is_active`, `is_staff`, `is_superuser`

## Testing

**Recommended test runner:** pytest

```bash
# Run all tests
docker compose run --rm backend sh -c 'pytest'

# Run specific test file
docker compose run --rm backend sh -c 'pytest core/tests/api/test_user.py'

# Run specific test class
docker compose run --rm backend sh -c 'pytest core/tests/api/test_user.py::PublicUserApiTest'

# Run with coverage report
docker compose run --rm backend sh -c 'pytest --cov'

# Run with verbose output
docker compose run --rm backend sh -c 'pytest -v'
```

**Alternative:** Django test runner

```bash
docker compose run --rm backend sh -c 'python manage.py test'
```

## Environment Variables

Configure via `.env` file in project root:

```env
# Database
DB_HOST=db
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres

# Django
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.local

# Server
NUMBER_OF_WORKERS=3
WORKERS_TIMEOUT=290

# Features
ADMIN_ENABLED=true
API_ENABLED=true

# CORS
CORS_ORIGIN_WHITELIST=http://localhost:3000,http://localhost:8080
```

## Key Technologies

- **Django 4.2 LTS** - Web framework
- **Django REST Framework 3.15** - API toolkit
- **PostgreSQL** - Database
- **pytest 8** - Testing framework
- **Factory Boy** - Test fixture generation
- **drf-yasg** - Swagger/OpenAPI documentation
- **Gunicorn 23** - WSGI HTTP server
- **python-json-logger** - Structured logging

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [pytest Documentation](https://docs.pytest.org/)
