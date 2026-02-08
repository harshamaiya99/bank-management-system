import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import DashboardLayout from "@/components/layout/DashboardLayout";
import LoginPage from "@/pages/LoginPage";
import DashboardPage from "@/pages/DashboardPage";
import CreateAccountPage from "@/pages/CreateAccountPage";
import AccountDetailsPage from "@/pages/AccountDetailsPage";
import { AuthProvider, useAuth } from "@/context/AuthContext";

const queryClient = new QueryClient();

// Protected Route utilizing useAuth
function ProtectedRoute() {
  const { isAuthenticated } = useAuth();
  // Use Outlet to render child routes if authenticated
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
}

// Public Route (redirects to dashboard if already logged in)
function PublicRoute() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Navigate to="/dashboard" replace /> : <Outlet />;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      {/* AuthProvider must be inside QueryClientProvider but outside Routes */}
      <AuthProvider>
        <BrowserRouter>
          <Routes>

            {/* Public Routes */}
            <Route element={<PublicRoute />}>
              <Route path="/login" element={<LoginPage />} />
            </Route>

            {/* Protected Routes */}
            <Route element={<ProtectedRoute />}>
              <Route element={<DashboardLayout />}>
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/create-account" element={<CreateAccountPage />} />
                <Route path="/account-details/:accountId" element={<AccountDetailsPage />} />
              </Route>
              {/* Catch root path and redirect to dashboard */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />

          </Routes>
          <Toaster />
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;