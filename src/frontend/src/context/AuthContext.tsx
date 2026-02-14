import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import api, { setMemoryToken } from "@/api/client"; // Import the setter
import { type AuthResponse } from "@/types";

interface AuthContextType {
  role: string | null;
  isAuthenticated: boolean;
  isLoading: boolean; // New state to prevent flickering
  login: (data: AuthResponse) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  // We only persist non-sensitive data like 'role' for UI logic
  const [role, setRole] = useState<string | null>(localStorage.getItem("role"));
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // 1. On App Load: Try to get a token using the HttpOnly Cookie
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // Try to refresh immediately
        const { data } = await api.post("/refresh");
        setMemoryToken(data.access_token);
        setRole(data.role);
        setIsAuthenticated(true);
      } catch (error) {
        // If refresh fails, user is truly logged out
        setRole(null);
        setIsAuthenticated(false);
        localStorage.removeItem("role");
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // 2. Login Action
  const login = (data: AuthResponse) => {
    setMemoryToken(data.access_token);
    setRole(data.role);
    setIsAuthenticated(true);

    // Only persist non-sensitive role
    localStorage.setItem("role", data.role);
    localStorage.setItem("process_id", crypto.randomUUID());
  };

  // 3. Logout Action
  const logout = async () => {
    try {
      await api.post("/logout"); // Tell backend to delete cookie
    } catch (e) {
      console.error("Logout failed", e);
    }
    setMemoryToken(null);
    setRole(null);
    setIsAuthenticated(false);
    localStorage.removeItem("role");
    localStorage.removeItem("process_id");
  };

  useEffect(() => {
    const handleUnauthorized = () => logout();
    window.addEventListener("auth:unauthorized", handleUnauthorized);
    return () => window.removeEventListener("auth:unauthorized", handleUnauthorized);
  }, []);

  return (
    <AuthContext.Provider value={{ role, isAuthenticated, isLoading, login, logout }}>
      {!isLoading && children}
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