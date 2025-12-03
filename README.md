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
│   ├── backend/        # Backend Dockerfile and entrypoint
│   └── frontend/       # Frontend Dockerfile and nginx config
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

**Backend commands**
```bash
# Run tests
docker compose run --rm backend sh -c 'pytest'

# Run migrations
docker compose run --rm backend sh -c 'python manage.py migrate'

# Create superuser
docker compose run --rm backend sh -c 'python manage.py createsuperuser'

# Access Django shell
docker compose run --rm backend sh -c 'python manage.py shell'
```

**Frontend commands**
```bash
# Install new package
docker compose exec frontend npm install <package-name>

# Run tests
docker compose exec frontend npm test

# Build for production
docker compose exec frontend npm run build
```

**Database**
```bash
# Reset database (removes all data)
docker compose down -v
```

## Development

Both backend and frontend support hot reload:

- **Backend**: Changes to `backend/` auto-reload Django dev server
- **Frontend**: Changes to `frontend/src/` auto-reload React dev server

## Documentation

Detailed documentation is available in each component:

- **Backend**: See [backend/README.md](backend/README.md) and [backend/CLAUDE.md](backend/CLAUDE.md)
- **Frontend**: See [frontend/README.md](frontend/README.md) and [frontend/CLAUDE.md](frontend/CLAUDE.md)

## Tech Stack

**Backend:**
- Django 4.2 LTS
- Django REST Framework 3.15
- PostgreSQL
- pytest 8
- Gunicorn 23

**Frontend:**
- React 18.2
- TypeScript 4.9.5
- React Router 6.20
- Tailwind CSS 3.3
- Axios 1.6

## Quick Test

1. Start services: `docker compose up`
2. Open http://localhost:3000
3. Register a new user
4. View dashboard and edit profile
5. Check Swagger API docs: http://localhost:8000/swagger/
