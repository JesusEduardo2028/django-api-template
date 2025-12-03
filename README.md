# Django API Template

A Django REST API template with PostgreSQL, Docker, pytest, and structured logging. Built with Django 4.2 LTS.

## Quick Start

**Build project**

```bash
docker-compose build
```

**Run local server**

```bash
docker-compose up
```

The server will be available at http://localhost:8000

## Testing

**Run all tests with pytest (recommended)**

```bash
docker-compose run --entrypoint="" backend sh -c 'cd /backend && pytest'
```

**Run tests with coverage**

```bash
docker-compose run --entrypoint="" backend sh -c 'cd /backend && pytest --cov'
```

**Run specific test file**

```bash
docker-compose run --entrypoint="" backend sh -c 'cd /backend && pytest core/tests/test_models.py'
```

**Run with Django's test runner and flake8**

```bash
docker-compose run backend sh -c 'python manage.py test && flake8'
```

## Development Commands

**Create superuser**

```bash
docker-compose run backend sh -c 'python manage.py createsuperuser'
```

**Run migrations**

```bash
docker-compose run backend sh -c 'python manage.py migrate'
```

**Create migrations**

```bash
docker-compose run backend sh -c 'python manage.py makemigrations'
```

**Access Django shell**

```bash
docker-compose run backend sh -c 'python manage.py shell'
```

## Project Structure

```
.
├── backend/              # Django application code
│   ├── config/          # Django settings and configuration
│   ├── core/            # Core app with User model and API
│   └── utils/           # Utilities (logging, etc.)
├── docker/              # Docker configuration
│   └── backend/         # Backend Dockerfile and entrypoint
├── docker-compose.yml   # Docker Compose configuration
├── pytest.ini           # Pytest configuration
└── requirements.txt     # Python dependencies
```