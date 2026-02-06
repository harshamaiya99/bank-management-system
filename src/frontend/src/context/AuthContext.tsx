import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { type AuthResponse } from "@/types";

interface AuthContextType {
  token: string | null;
  role: string | null;
  isAuthenticated: boolean;
  login: (data: AuthResponse) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  // Initialize state from localStorage to persist auth on reload
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [role, setRole] = useState<string | null>(localStorage.getItem("role"));

  const isAuthenticated = !!token;

  const login = (data: AuthResponse) => {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", data.role);
    // Process ID can be managed here or in the interceptor
    localStorage.setItem("process_id", crypto.randomUUID());

    setToken(data.access_token);
    setRole(data.role);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("process_id");
    setToken(null);
    setRole(null);
  };

  // Listen for 401 Unauthorized events from the Axios interceptor
  useEffect(() => {
    const handleUnauthorized = () => logout();
    window.addEventListener("auth:unauthorized", handleUnauthorized);
    return () => window.removeEventListener("auth:unauthorized", handleUnauthorized);
  }, []);

  return (
    <AuthContext.Provider value={{ token, role, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}