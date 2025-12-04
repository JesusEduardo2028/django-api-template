# Frontend - CLAUDE.md

This file provides guidance to Claude Code when working with the React frontend.

## Architecture Overview

React 18 + TypeScript frontend with:
- Token-based authentication with Django backend
- React Context API for global auth state
- React Router v6 for client-side routing
- Axios for HTTP requests with interceptors
- Tailwind CSS for styling
- Docker containerization with hot reload

## Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML template with root div
├── src/
│   ├── api/                    # API client layer
│   │   ├── client.ts          # Axios instance, interceptors, base config
│   │   ├── types.ts           # TypeScript interfaces (User, AuthToken, etc.)
│   │   └── auth.ts            # Auth API functions (login, register, etc.)
│   ├── context/
│   │   └── AuthContext.tsx    # Auth state provider, useAuth hook
│   ├── pages/                  # Page components
│   │   ├── Login.tsx          # Login form with error handling
│   │   ├── Register.tsx       # Registration form with validation
│   │   ├── Dashboard.tsx      # User dashboard (protected)
│   │   └── Profile.tsx        # Edit profile (protected)
│   ├── utils/                  # Utility functions
│   │   ├── constants.ts       # ROUTES and API_ENDPOINTS constants
│   │   └── storage.ts         # Token management (localStorage)
│   ├── App.tsx                 # Main app, routing, route guards
│   ├── index.tsx              # React entry point, renders App
│   └── index.css              # Tailwind imports, custom utilities
├── .env.development            # Dev environment vars
├── .env.production             # Prod environment vars
├── package.json                # Dependencies, scripts, proxy config
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.js          # Tailwind theme customization
└── postcss.config.js           # PostCSS plugins
```

## Key Files

### API Client (src/api/client.ts)

**Axios Instance**:
- Base URL from environment: `process.env.REACT_APP_API_URL`
- Timeout: 10 seconds
- Default headers: `Content-Type: application/json`

**Request Interceptor**:
- Adds `Authorization: Token <token>` header to all requests
- Reads token from localStorage via `getToken()`

**Response Interceptor**:
- Handles 401 errors (unauthorized)
- Clears token and redirects to login on 401
- Allows error propagation for handling in components

### API Functions (src/api/auth.ts)

Exports `authApi` object with methods:
- `register(userData)` - POST /api/core/create/
- `login(credentials)` - POST /api/core/token/
- `getCurrentUser()` - GET /api/core/me/
- `updateUser(userData)` - PATCH /api/core/me/

All functions return typed responses using interfaces from `types.ts`.

### Type Definitions (src/api/types.ts)

Key interfaces:
- `User` - User data (id, email, name)
- `UserCreate` - Registration payload
- `UserUpdate` - Profile update payload
- `LoginCredentials` - Login payload
- `AuthToken` - Token response

### Authentication Context (src/context/AuthContext.tsx)

**State**:
- `user: User | null` - Current user data
- `loading: boolean` - Initial load state
- `isAuthenticated: boolean` - Computed from user presence

**Methods**:
- `login(email, password)` - Authenticate and set user
- `logout()` - Clear token and user
- `register(email, password, name)` - Create user and auto-login
- `updateUser(userData)` - Update user profile

**Initialization**:
- On mount, checks for token in localStorage
- If token exists, fetches user data
- Sets loading to false after check

**Custom Hook**: `useAuth()` - Access auth context in components

### Token Storage (src/utils/storage.ts)

Functions for localStorage management:
- `getToken()` - Get auth token
- `setToken(token)` - Save auth token
- `clearToken()` - Remove auth token
- `isAuthenticated()` - Check if token exists

Key: `auth_token`

### Constants (src/utils/constants.ts)

**ROUTES**:
- HOME: `/`
- LOGIN: `/login`
- REGISTER: `/register`
- DASHBOARD: `/dashboard`
- PROFILE: `/profile`

**API_ENDPOINTS**:
- CREATE_USER: `/core/create/`
- TOKEN: `/core/token/`
- ME: `/core/me/`

### Main App (src/App.tsx)

**Route Guards**:

`ProtectedRoute`:
- Requires authentication
- Shows loading spinner while checking auth
- Redirects to login if not authenticated

`PublicRoute`:
- For login/register pages
- Redirects to dashboard if already authenticated

**Routes**:
- `/` - Redirects to dashboard
- `/login` - PublicRoute → Login
- `/register` - PublicRoute → Register
- `/dashboard` - ProtectedRoute → Dashboard
- `/profile` - ProtectedRoute → Profile
- `*` - Catch-all redirects to home

**Structure**:
- `Router` wraps everything
- `AuthProvider` wraps routes
- `AppRoutes` component contains all route definitions

## Page Components

### Login (src/pages/Login.tsx)

- Email and password form
- Error display from API
- Loading state during submission
- Link to Register page
- Redirects to Dashboard on success

### Register (src/pages/Register.tsx)

- Name, email, password, confirm password form
- Client-side validation:
  - Password match check
  - Minimum 5 characters
- Error display from API
- Auto-login after successful registration
- Link to Login page

### Dashboard (src/pages/Dashboard.tsx)

- Displays user information (name, email, ID)
- Navigation bar with logout button
- Link to Profile page
- Protected route (requires auth)

### Profile (src/pages/Profile.tsx)

- Edit name and email form
- Success/error message display
- Back to Dashboard link
- Navigation bar with logout button
- Protected route (requires auth)

## Styling

### Tailwind Configuration (tailwind.config.js)

**Content Paths**:
- `./src/**/*.{js,jsx,ts,tsx}`
- `./public/index.html`

**Theme Extensions**:
- Custom primary color palette (blue shades)

### Custom Utilities (src/index.css)

**Buttons**:
- `.btn` - Base button (padding, rounded, transitions)
- `.btn-primary` - Blue background, white text
- `.btn-secondary` - Gray background, dark text

**Forms**:
- `.input` - Full width, border, focus ring

**Layout**:
- `.card` - White background, rounded, shadow, padding

## Development Workflow

### Running the Frontend

From project root:
```bash
# Start with docker compose (recommended)
docker compose up frontend

# Or start all services
docker compose up
```

Runs on http://localhost:3000

### Making Changes

1. **Edit files** in `frontend/src/`
   - Changes auto-reload in browser (hot reload enabled)

2. **Add new components**:
   - Create in `src/components/` directory
   - Import in page components

3. **Add new pages**:
   - Create in `src/pages/`
   - Add route in `src/App.tsx`
   - Add constant in `src/utils/constants.ts`

4. **Add new API calls**:
   - Define TypeScript interface in `src/api/types.ts`
   - Add function in appropriate API file (e.g., `auth.ts`)
   - Use in components via async/await

### Installing Packages

```bash
# Install runtime dependency
docker compose exec frontend npm install <package-name>

# Install dev dependency
docker compose exec frontend npm install -D <package-name>
```

After installation, rebuild container if package.json changed:
```bash
docker compose build frontend
```

### Testing API Integration

1. Ensure backend is running on port 8000
2. Check CORS settings in backend allow localhost:3000
3. Use browser DevTools Network tab to debug API calls
4. Check localStorage for token persistence

## Common Tasks

### Add New Route

1. **Define route constant** in `src/utils/constants.ts`:
   ```typescript
   export const ROUTES = {
     // ... existing routes
     NEW_PAGE: '/new-page',
   } as const;
   ```

2. **Create page component** in `src/pages/NewPage.tsx`

3. **Add route** in `src/App.tsx`:
   ```tsx
   <Route
     path={ROUTES.NEW_PAGE}
     element={
       <ProtectedRoute>
         <NewPage />
       </ProtectedRoute>
     }
   />
   ```

### Add New API Endpoint

1. **Define types** in `src/api/types.ts`:
   ```typescript
   export interface NewData {
     field: string;
   }
   ```

2. **Add API function** in appropriate file (or create new):
   ```typescript
   export const newApi = {
     getData: async (): Promise<NewData> => {
       const response = await apiClient.get('/api/endpoint/');
       return response.data;
     },
   };
   ```

3. **Use in component**:
   ```typescript
   const [data, setData] = useState<NewData | null>(null);
   useEffect(() => {
     const fetchData = async () => {
       const result = await newApi.getData();
       setData(result);
     };
     fetchData();
   }, []);
   ```

### Handle Form Submission

Pattern used throughout the app:
```typescript
const [formData, setFormData] = useState('');
const [error, setError] = useState('');
const [loading, setLoading] = useState(false);

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setError('');
  setLoading(true);

  try {
    await apiFunction(formData);
    // Handle success
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || 'Error message';
    setError(errorMsg);
  } finally {
    setLoading(false);
  }
};
```

## Important Notes

### TypeScript Version

- Using TypeScript 4.9.5 (not 5.x)
- Required for compatibility with react-scripts 5.0.1
- DO NOT upgrade to TypeScript 5.x without upgrading CRA

### Authentication Token

- Stored in localStorage with key `auth_token`
- Automatically added to all API requests via interceptor
- Cleared on 401 response or logout
- Format: `Token <token-value>` (Django REST Framework format)

### CORS

- Backend must include frontend URL in CORS whitelist
- Location: `backend/config/settings/base.py:175-177`
- Must include: `http://localhost:3000`
- `CORS_ALLOW_CREDENTIALS = True` required for token auth

### Hot Reload

- Enabled via volume mounts in docker-compose.yml
- `CHOKIDAR_USEPOLLING=true` for Docker compatibility
- Changes to `src/` files auto-reload
- Changes to `public/` require restart

### React Router v6

- Uses `element` prop (not `component`)
- Navigate programmatically with `useNavigate()` hook
- Protect routes with wrapper components (not HOCs)

### Error Handling

- API errors display in components with error state
- 401 errors handled globally by interceptor
- Component-level try/catch for specific error messages
- Check `err.response?.data?.detail` for Django error messages

## Environment Variables

Access with `process.env.REACT_APP_*`:
- `REACT_APP_API_URL` - Backend API base URL

All custom env vars must start with `REACT_APP_`.

## Docker Configuration

**Dockerfile** (`../docker/frontend/Dockerfile`):
- Base: node:18-alpine
- Copies package.json, runs npm install
- Copies frontend code
- Exposes port 3000
- Starts dev server with `npm start`

**docker-compose.yml** frontend service:
- Volume mounts for hot reload
- Anonymous volume for node_modules
- Polling enabled for Docker compatibility
- Depends on backend service

## Common Issues

### "getToken is defined but never used"
- Fixed: Removed unused import from AuthContext.tsx
- Only import what's actually used in the file

### TypeScript Errors
- Check tsconfig.json for strict settings
- Ensure proper typing on all functions/variables
- Use interfaces from types.ts

### API Requests Failing
1. Check backend is running: `docker compose ps`
2. Check CORS configuration in backend
3. Check token in localStorage
4. Check Network tab for actual error response

### Styling Not Updating
- Ensure Tailwind content paths include your files
- Check PostCSS configuration
- Rebuild if necessary: `docker compose build frontend`

## Testing Integration

To test the full flow:
1. Start services: `docker compose up`
2. Open http://localhost:3000
3. Register new user
4. Should auto-redirect to dashboard
5. Edit profile
6. Logout
7. Login with credentials
8. Check localStorage for token

## Future Improvements

Consider migrating from Create React App to Vite:
- Faster build times
- Better hot reload
- Modern build tooling
- TypeScript 5.x support

CRA is in maintenance mode but stable for current use.
