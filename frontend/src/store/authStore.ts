import { create } from 'zustand';
import { User, clearStorage, saveUserToStorage } from '../api/auth';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,

  setUser: (user: User, token: string) => {
    saveUserToStorage(user, token);
    set({ user, isAuthenticated: true });
  },

  logout: () => {
    clearStorage();
    set({ user: null, isAuthenticated: false });
  },
}));
