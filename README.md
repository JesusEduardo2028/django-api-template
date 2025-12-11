# Django API Template

Full-stack application with Django REST API backend and React TypeScript frontend.

## Project Structure

```
django-api-template/
├── backend/              # Django 4.2 LTS REST API
│   ├── config/          # Settings and configuration
│   ├── core/            # Core app with User model and API
│   ├── utils/           # Utilities (logging, etc.)
│   ├── README.md        # Backend documentation
│   └── CLAUDE.md        # Backend development guide
├── frontend/            # React + TypeScript + Tailwind CSS
│   ├── src/
│   │   ├── api/        # API client layer
│   │   ├── context/    # React Context (auth)
│   │   ├── pages/      # Page components
│   │   └── utils/      # Utilities
│   ├── README.md        # Frontend documentation
│   └── CLAUDE.md        # Frontend development guide
├── docker/              # Docker configuration files
│   ├── backend/        # Backend Dockerfile and entr`ypoint
│   ├── frontend/       # Frontend Dockerfile and nginx config
└── docker-compose.yml   # Services orchestration
```

## Services

- **Backend**: http://localhost:8000 (Django REST API)
- **Frontend**: http://localhost:3000 (React application)
- **Database**: PostgreSQL on port 5432
- **API Docs**: http://localhost:8000/swagger/

## Quick Start

**Build all services**
```bash
docker compose build
```

**Start all services**
```bash
docker compose up
```

**Start in detached mode**
```bash
docker compose up -d
```

**Stop services**
```bash
docker compose down
```

**View logs**
```bash
docker compose logs -f              # All services
docker compose logs -f backend      # Backend only
docker compose logs -f frontend     # Frontend only
```

## Common Commands

```bash
# Reset database (removes all data)
docker compose down -v
```

**Backend commands**: See `backend/README.md` (tests, migrations, Django shell, etc.)

**Frontend commands**: See `frontend/README.md` (npm install, tests, build, etc.)

## Development

Both backend and frontend support hot reload:

- **Backend**: Changes to `backend/` auto-reload Django dev server
- **Frontend**: Changes to `frontend/src/` auto-reload React dev server

## Documentation

Detailed documentation is available in each component:

- **Backend**: See [backend/README.md](backend/README.md) and [backend/CLAUDE.md](backend/CLAUDE.md)
- **Frontend**: See [frontend/README.md](frontend/README.md) and [frontend/CLAUDE.md](frontend/CLAUDE.md)

## Tech Stack

- **Backend**: Django 4.2 LTS + Django REST Framework + PostgreSQL
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Infrastructure**: Docker + Docker Compose

See `backend/README.md` and `frontend/README.md` for detailed dependency versions.

## Quick Test

1. Start services: `docker compose up`
2. Open http://localhost:3000
3. Register a new user
4. View dashboard and edit profile
5. Check Swagger API docs: http://localhost:8000/swagger/
