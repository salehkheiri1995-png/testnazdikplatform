import axiosClient from './axiosClient';

export interface User {
  id: number;
  full_name: string;
  phone: string;
  email?: string;
  role: string;
}

export interface LoginRequest {
  phone: string;
  password: string;
}

export interface RegisterRequest {
  full_name: string;
  phone: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const login = async (data: LoginRequest): Promise<AuthResponse> => {
  const res = await axiosClient.post<AuthResponse>('/api/v1/auth/login', data);
  return res.data;
};

export const register = async (data: RegisterRequest): Promise<AuthResponse> => {
  const res = await axiosClient.post<AuthResponse>('/api/v1/auth/register', data);
  return res.data;
};

export const getUserFromStorage = (): User | null => {
  try {
    const raw = localStorage.getItem('user');
    if (!raw) return null;
    return JSON.parse(raw) as User;
  } catch {
    return null;
  }
};

export const saveUserToStorage = (user: User, token: string) => {
  localStorage.setItem('user', JSON.stringify(user));
  localStorage.setItem('access_token', token);
};

export const clearStorage = () => {
  localStorage.removeItem('user');
  localStorage.removeItem('access_token');
};
