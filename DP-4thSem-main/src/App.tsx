import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/auth/ProtectedRoute';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import UserLayout from './components/layout/UserLayout';
import UserComplaintHistory from './pages/UserComplaintHistory';
import AIChatIntake from './pages/AIChatIntake';
import AdminLayout from './components/layout/AdminLayout';
import AdminDashboard from './pages/AdminDashboard';
import AdminComplaintConsole from './pages/AdminComplaintConsole';
import ProviderSelection from './pages/ProviderSelection';

function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />

      {/* User routes */}
      <Route
        path="/user"
        element={
          <ProtectedRoute allowedRoles={['user']}>
            <UserLayout />
          </ProtectedRoute>
        }
      >
        <Route path="history" element={<UserComplaintHistory />} />
        <Route path="chat" element={<AIChatIntake />} />
      </Route>

      {/* Admin routes */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute allowedRoles={['admin', 'super_admin']}>
            <AdminLayout />
          </ProtectedRoute>
        }
      >
        <Route path="dashboard" element={<AdminDashboard />} />
        <Route path="complaints" element={<AdminComplaintConsole />} />
        <Route path="complaints/:id/providers" element={<ProviderSelection />} />
      </Route>
    </Routes>
  );
}

export default App;
