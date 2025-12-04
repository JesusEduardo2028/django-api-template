# React Frontend

React + TypeScript + Tailwind CSS frontend for the Django API Template.

## Quick Start

**From project root directory:**

```bash
# Build frontend
docker compose build frontend

# Start all services (frontend will run on http://localhost:3000)
docker compose up

# Start only frontend (requires backend to be running)
docker compose up frontend
```

Visit http://localhost:3000 to access the application.

## Features

- **Authentication**: Complete login/registration flow with token-based auth
- **User Management**: View and edit user profile
- **Protected Routes**: Automatic redirect for authenticated/unauthenticated users
- **API Integration**: Centralized Axios client with request/response interceptors
- **Type Safety**: Full TypeScript coverage
- **Styling**: Tailwind CSS with custom utility classes
- **Hot Reload**: Instant updates during development

## Application Structure

```
frontend/
├── public/               # Static files
│   └── index.html       # HTML template
├── src/
│   ├── api/             # API client layer
│   │   ├── client.ts   # Axios instance with interceptors
│   │   ├── types.ts    # TypeScript interfaces
│   │   └── auth.ts     # Authentication API calls
│   ├── context/         # React Context
│   │   └── AuthContext.tsx  # Authentication state
│   ├── pages/           # Page components
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   └── Profile.tsx
│   ├── utils/           # Utility functions
│   │   ├── constants.ts # Routes and constants
│   │   └── storage.ts  # Token storage
│   ├── App.tsx          # Main app with routing
│   ├── index.tsx        # React entry point
│   └── index.css        # Tailwind CSS imports
├── .env.development     # Development environment variables
├── .env.production      # Production environment variables
├── package.json         # Dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── tailwind.config.js   # Tailwind CSS configuration
└── postcss.config.js    # PostCSS configuration
```

## Pages

### Public Routes

- **Login** (`/login`) - Email and password authentication
- **Register** (`/register`) - User registration with name, email, password

### Protected Routes (Require Authentication)

- **Dashboard** (`/dashboard`) - User information display
- **Profile** (`/profile`) - Edit user name and email

## API Integration

The frontend connects to the Django backend API:

- **Base URL**: `http://localhost:8000` (configured via proxy in package.json)
- **Authentication**: Token-based with `Authorization: Token <token>` header
- **Token Storage**: localStorage (key: `auth_token`)

### API Endpoints Used

- `POST /api/core/create/` - User registration
- `POST /api/core/token/` - Login and token generation
- `GET /api/core/me/` - Get current user
- `PATCH /api/core/me/` - Update user profile

## Development Commands

### Installing Dependencies

```bash
# Install new package
docker compose exec frontend npm install <package-name>

# Install dev dependency
docker compose exec frontend npm install -D <package-name>
```

### Running Scripts

```bash
# Start development server (already runs with docker-compose up)
docker compose exec frontend npm start

# Run tests
docker compose exec frontend npm test

# Build for production
docker compose exec frontend npm run build

# Access container shell
docker compose exec frontend sh
```

### Viewing Logs

```bash
# Follow frontend logs
docker compose logs frontend --follow

# View last 50 lines
docker compose logs frontend --tail 50
```

## Custom Tailwind Classes

The project includes custom utility classes defined in `src/index.css`:

### Buttons
- `.btn` - Base button styles
- `.btn-primary` - Primary button (blue)
- `.btn-secondary` - Secondary button (gray)

### Forms
- `.input` - Form input styles

### Layout
- `.card` - Card container with shadow

## Environment Variables

**Development** (`.env.development`):
```env
REACT_APP_API_URL=http://localhost:8000
```

**Production** (`.env.production`):
```env
REACT_APP_API_URL=https://your-api-domain.com
```

## Technology Stack

- **React 18.2** - UI library
- **TypeScript 4.9.5** - Type safety
- **React Router 6.20** - Client-side routing
- **Axios 1.6** - HTTP client
- **Tailwind CSS 3.3** - Utility-first CSS
- **Create React App 5.0.1** - Build tooling

## Authentication Flow

1. **Registration**:
   - User submits registration form
   - API creates user account
   - Auto-login after successful registration
   - Redirect to dashboard

2. **Login**:
   - User submits email and password
   - API returns authentication token
   - Token stored in localStorage
   - User data fetched and stored in context
   - Redirect to dashboard

3. **Protected Routes**:
   - Check for valid token on route access
   - Fetch user data if token exists
   - Redirect to login if not authenticated

4. **Logout**:
   - Clear token from localStorage
   - Clear user from context
   - Redirect to login page

## Hot Reload

The development server supports hot reload for instant updates:

- **React Components**: Changes reflect immediately
- **Tailwind CSS**: Style updates reflect immediately
- **TypeScript**: Automatic type checking on save

Docker volume configuration ensures hot reload works correctly:
- Source files mounted: `./frontend:/app`
- Node modules excluded: `/app/node_modules` (anonymous volume)
- Polling enabled: `CHOKIDAR_USEPOLLING=true`, `WATCHPACK_POLLING=true`

## Building for Production

```bash
# Build production bundle
docker compose exec frontend npm run build

# Output will be in frontend/build/
```

The production build:
- Minifies JavaScript and CSS
- Optimizes images
- Generates source maps
- Creates static HTML, CSS, and JS files

Serve the `build/` directory with Nginx (see `../docker/frontend/nginx.conf`).

## Common Issues

### Hot Reload Not Working
Ensure environment variables are set:
- `CHOKIDAR_USEPOLLING=true`
- `WATCHPACK_POLLING=true`

### CORS Errors
Check that the backend has CORS configured for `http://localhost:3000`:
- Backend setting: `CORS_ORIGIN_WHITELIST` in `backend/config/settings/base.py`

### Token Not Persisting
Check browser's localStorage:
1. Open DevTools (F12)
2. Go to Application tab
3. Check localStorage for `auth_token` key

### API Connection Refused
Ensure backend is running:
```bash
docker compose ps
```
Backend should be running on port 8000.

## Additional Resources

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [React Router Documentation](https://reactrouter.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Axios Documentation](https://axios-http.com/docs/intro)
