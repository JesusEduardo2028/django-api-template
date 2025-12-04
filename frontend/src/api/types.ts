// API Type Definitions matching Django models

export interface User {
  id: string;
  email: string;
  name: string;
}

export interface UserCreate {
  email: string;
  password: string;
  name: string;
}

export interface UserUpdate {
  email?: string;
  name?: string;
  password?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthToken {
  token: string;
}

export interface ApiError {
  detail?: string;
  [key: string]: any;
}
