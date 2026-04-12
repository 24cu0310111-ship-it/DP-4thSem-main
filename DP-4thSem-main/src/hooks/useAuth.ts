import { useState, useEffect, useCallback } from 'react';
import type { AuthState, LoginRequest, User, UserRole } from '../types';
import { authService } from '../services/authService';

const STORAGE_KEYS = {
  token: 'scms_token',
  refreshToken: 'scms_refresh_token',
  user: 'scms_user',
} as const;

function getStoredAuth(): AuthState {
  try {
    const token = localStorage.getItem(STORAGE_KEYS.token);
    const userStr = localStorage.getItem(STORAGE_KEYS.user);
    const user = userStr ? JSON.parse(userStr) as User : null;
    return {
      user,
      token,
      isAuthenticated: !!token && !!user,
      isLoading: false,
    };
  } catch {
    return { user: null, token: null, isAuthenticated: false, isLoading: false };
  }
}

export function useAuth() {
  const [authState, setAuthState] = useState<AuthState>(() => ({
    ...getStoredAuth(),
    isLoading: true,
  }));

  useEffect(() => {
    const stored = getStoredAuth();
    setAuthState({ ...stored, isLoading: false });
  }, []);

  const login = useCallback(async (credentials: LoginRequest) => {
    setAuthState((prev) => ({ ...prev, isLoading: true }));
    try {
      const response = await authService.login(credentials);

      const user: User = {
        id: response.user.id,
        name: response.user.name,
        role: response.user.role,
        phone: credentials.phone,
        is_active: true,
        address: { flat_no: '', building: '', area: '', city: '', pincode: '' },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      localStorage.setItem(STORAGE_KEYS.token, response.access_token);
      localStorage.setItem(STORAGE_KEYS.refreshToken, response.refresh_token);
      localStorage.setItem(STORAGE_KEYS.user, JSON.stringify(user));

      setAuthState({
        user,
        token: response.access_token,
        isAuthenticated: true,
        isLoading: false,
      });

      return user;
    } catch (error) {
      setAuthState({ user: null, token: null, isAuthenticated: false, isLoading: false });
      throw error;
    }
  }, []);

  const logout = useCallback(() => {
    authService.logout();
    setAuthState({ user: null, token: null, isAuthenticated: false, isLoading: false });
  }, []);

  const hasRole = useCallback(
    (role: UserRole) => authState.user?.role === role,
    [authState.user]
  );

  return {
    ...authState,
    login,
    logout,
    hasRole,
    isAdmin: authState.user?.role === 'admin' || authState.user?.role === 'super_admin',
    isUser: authState.user?.role === 'user',
  };
}
