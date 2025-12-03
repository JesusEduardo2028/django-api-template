import apiClient from './client';
import { User, UserCreate, UserUpdate, LoginCredentials, AuthToken } from './types';

export const authApi = {
  // POST /api/core/create/
  register: async (userData: UserCreate): Promise<User> => {
    const response = await apiClient.post<User>('/core/create/', userData);
    return response.data;
  },

  // POST /api/core/token/
  login: async (credentials: LoginCredentials): Promise<AuthToken> => {
    const response = await apiClient.post<AuthToken>('/core/token/', credentials);
    return response.data;
  },

  // GET /api/core/me/
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/core/me/');
    return response.data;
  },

  // PUT/PATCH /api/core/me/
  updateUser: async (userData: UserUpdate): Promise<User> => {
    const response = await apiClient.patch<User>('/core/me/', userData);
    return response.data;
  },
};
