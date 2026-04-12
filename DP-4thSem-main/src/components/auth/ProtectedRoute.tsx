import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import type { UserRole } from '../../types';

interface ProtectedRouteProps {
  readonly children: React.ReactNode;
  readonly allowedRoles?: UserRole[];
}

export default function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#121318] flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 border-2 border-[#bbc3ff] border-t-transparent rounded-full animate-spin" />
          <p className="text-[#c6c5d0] font-label text-sm uppercase tracking-wider">
            Validating session...
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && user && !allowedRoles.includes(user.role)) {
    // Redirect to appropriate home based on role
    const redirectTo = user.role === 'admin' || user.role === 'super_admin'
      ? '/admin/dashboard'
      : '/user/history';
    return <Navigate to={redirectTo} replace />;
  }

  return <>{children}</>;
}
