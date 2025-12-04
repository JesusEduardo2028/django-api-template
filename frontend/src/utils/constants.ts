export const APP_NAME = 'Django Template';

export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
} as const;

export const API_ENDPOINTS = {
  CREATE_USER: '/core/create/',
  TOKEN: '/core/token/',
  ME: '/core/me/',
} as const;
