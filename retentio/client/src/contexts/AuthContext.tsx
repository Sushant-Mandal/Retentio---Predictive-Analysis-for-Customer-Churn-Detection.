/** Signal in the Dark: API-connected auth boundary with persistent token storage. */
import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { authApi, TOKEN_KEY } from '@/lib/api';
import type { User } from '@/lib/types';

type AuthContextValue = {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (input: { name: string; businessName: string; email: string; password: string }) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  setUser: (u: User) => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY));
  const [isLoading, setIsLoading] = useState(true);

  // Restore user from token on mount
  useEffect(() => {
    if (token) {
      authApi.me()
        .then(setUser)
        .catch(() => {
          setToken(null);
          localStorage.removeItem(TOKEN_KEY);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [token]);

  const login = async (email: string, password: string) => {
    const res = await authApi.login(email, password);
    setToken(res.token);
    setUser(res.user);
    localStorage.setItem(TOKEN_KEY, res.token);
  };

  const signup = async (input: { name: string; businessName: string; email: string; password: string }) => {
    const res = await authApi.signup({
      business_name: input.businessName,
      name: input.name,
      email: input.email,
      password: input.password
    });
    setToken(res.token);
    setUser(res.user);
    localStorage.setItem(TOKEN_KEY, res.token);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem(TOKEN_KEY);
  };

  const value = useMemo(() => ({
    user, token, isAuthenticated: Boolean(token), login, signup, logout, isLoading, setUser
  }), [user, token, isLoading]);

  if (isLoading) {
    return null; // Or a loading spinner
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth must be used inside AuthProvider');
  return value;
}
