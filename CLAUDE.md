# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

Full-stack web application with Django REST API backend and React TypeScript frontend, containerized with Docker.

**Stack:**
- **Backend**: Django 4.2 LTS + Django REST Framework 3.15
- **Frontend**: React 18.2 + TypeScript 4.9.5 + Tailwind CSS 3.3
- **Database**: PostgreSQL
- **Infrastructure**: Docker + Docker Compose

**Communication Flow:**
```
Frontend (React :3000)
    ↓ HTTP + Axios
Backend (Django :8000)
    ↓ psycopg2
Database (PostgreSQL :5432)
```

## Project Structure

```
django-api-template/
├── backend/              # Django REST API (see backend/CLAUDE.md)
├── frontend/            # React + TypeScript (see frontend/CLAUDE.md)
├── docker/              # Dockerfiles and entrypoints
└── docker-compose.yml   # Service orchestration
```

**Detailed documentation:**
- Backend: See `backend/README.md` and `backend/CLAUDE.md`
- Frontend: See `frontend/README.md` and `frontend/CLAUDE.md`

## Common Commands

All commands run from project root.

### Service Management

```bash
# Start all services
docker compose up

# Start in detached mode
docker compose up -d

# Stop services
docker compose down

# Reset database (removes all data)
docker compose down -v

# View logs
docker compose logs -f              # All services
docker compose logs -f backend      # Backend only
docker compose logs -f frontend     # Frontend only

# Rebuild after dependency changes
docker compose build
```

### Component-Specific Commands

For backend commands (tests, migrations, Django shell, etc.), see `backend/README.md`

For frontend commands (npm install, tests, build, etc.), see `frontend/README.md`

## Authentication Architecture

Token-based authentication using Django REST Framework's built-in token system.

### High-Level Flow

1. **User registers** → Backend creates user → Returns user data
2. **User logs in** → Backend returns auth token → Frontend stores in localStorage
3. **Subsequent requests** → Frontend adds `Authorization: Token <value>` header
4. **Token validation** → Backend validates token → Returns user data or 401
5. **401 response** → Frontend clears token → Redirects to login

### Key Integration Points

**Backend** (`backend/core/`):
- Custom User model with UUID and email authentication
- API endpoints: `/api/core/create/`, `/api/core/token/`, `/api/core/me/`
- CORS configured to allow frontend on `http://localhost:3000`
- See `backend/CLAUDE.md` for implementation details

**Frontend** (`frontend/src/`):
- Token stored in localStorage (key: `auth_token`)
- Axios interceptors handle auth header and 401 responses
- AuthContext provides global auth state
- Route guards protect authenticated pages
- See `frontend/CLAUDE.md` for implementation details

## Database Schema

Custom User model with UUID primary key and email authentication. See `backend/CLAUDE.md` for detailed schema.

## Docker Configuration

### Service Communication

Services communicate via Docker's internal network using service names:
- Frontend → Backend: `http://backend:8000`
- Backend → Database: `db:5432`

### Entrypoint Behavior (`docker/backend/entrypoint.sh`)

The backend entrypoint performs automatic setup:
1. Waits for database readiness using `wait-for-it db:5432 --timeout=30`
2. Runs migrations: `python manage.py migrate`
3. Starts server based on command:
   - `django` - Django dev server (default for development)
   - `ddtrace-gunicorn` - Gunicorn with DataDog APM
   - Default - Gunicorn production server

### Hot Reload

Both services support live code updates via volume mounts and auto-reload configured in `docker-compose.yml`.

## Development Workflow

### Adding New Features

**Backend**: See `backend/CLAUDE.md` for detailed workflow (models → serializers → views → URLs → tests)

**Frontend**: See `frontend/CLAUDE.md` for detailed workflow (types → API functions → components → routes)

### Database Migrations

```bash
docker compose run --rm backend sh -c 'python manage.py makemigrations'
docker compose run --rm backend sh -c 'python manage.py migrate'
```

See `backend/README.md` for more migration commands.

### Installing Dependencies

**Backend**: Add to `requirements.txt`, then `docker compose build backend`

**Frontend**: `docker compose exec frontend npm install <package>`, then rebuild if needed

## Testing

**Backend**: pytest with Factory Boy for test data. Run `docker compose run --rm backend sh -c 'pytest'`

**Frontend**: Jest via react-scripts. Run `docker compose exec frontend npm test`

See `backend/CLAUDE.md` and `frontend/CLAUDE.md` for detailed testing workflows.

## API Documentation

**Swagger UI**: http://localhost:8000/swagger/
**ReDoc**: http://localhost:8000/redoc/
**OpenAPI Schema**: http://localhost:8000/api/schema/

Configured with `drf-spectacular` in `backend/config/urls.py`.
Bearer token authentication supported in Swagger UI.

## Important Notes

### Custom User Model
The project uses a custom User model with **email authentication** (not username) and **UUID primary key**. This cannot be changed after initial migrations. See `backend/CLAUDE.md` for details.

### CORS Configuration
Critical for frontend-backend communication. Backend must allow `http://localhost:3000`. Configured in `backend/config/settings/base.py`. See `backend/CLAUDE.md` for details.

### TypeScript Version Constraint
Frontend uses TypeScript 4.9.5 (not 5.x) for Create React App compatibility. See `frontend/CLAUDE.md` for details.

## Common Issues

### Services Not Starting
Check service status: `docker compose ps`
View logs: `docker compose logs -f [service-name]`

### Frontend Can't Connect to Backend
1. Ensure backend is running on port 8000
2. Check CORS allows `http://localhost:3000` (see `backend/config/settings/base.py`)
3. Check browser console and Network tab for errors

### Database Connection Issues
Backend waits 30s for database at startup. If it fails, check: `docker compose logs db`

**Component-specific issues**: See `backend/CLAUDE.md` and `frontend/CLAUDE.md`

## Services

When running `docker compose up`, access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **PostgreSQL**: localhost:5432 (credentials in docker-compose.yml)

## Quick Test Flow

Test the full authentication flow:
1. Start services: `docker compose up`
2. Open http://localhost:3000
3. Register new user (auto-logs in)
4. View dashboard, edit profile, logout, login
5. Check Swagger docs: http://localhost:8000/swagger/
