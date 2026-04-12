import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useState } from 'react';

const NAV_ITEMS = [
  { path: '/user/history', label: 'Complaints', icon: 'history' },
  { path: '/user/chat', label: 'AI Chat', icon: 'smart_toy' },
];

export default function UserLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-surface flex">
      {/* Sidebar — desktop */}
      <aside className="hidden md:flex w-64 flex-col bg-surface-container-low border-r border-outline-variant/10 p-6">
        <div className="mb-10">
          <NavLink to="/" className="text-xl font-display font-bold text-on-surface hover:text-primary-container transition-colors">
            SCMS
          </NavLink>
          <p className="text-xs text-on-surface-variant mt-1 label-caps">User Portal</p>
        </div>

        <nav className="flex-1 space-y-1">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-obsidian text-sm font-body transition-all duration-200 ${
                  isActive
                    ? 'bg-primary-container/15 text-primary-container'
                    : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'
                }`
              }
            >
              <span className="material-symbols-outlined text-xl">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-outline-variant/10 pt-4 mt-4">
          <div className="flex items-center gap-3 px-4 py-2">
            <div className="w-8 h-8 rounded-full bg-secondary-container flex items-center justify-center text-sm font-semibold text-on-secondary">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-on-surface truncate">{user?.name || 'User'}</p>
              <p className="text-xs text-on-surface-variant truncate">{user?.phone}</p>
            </div>
          </div>
          <button onClick={handleLogout} className="flex items-center gap-3 px-4 py-3 rounded-obsidian text-sm text-error hover:bg-error-container/10 transition-all w-full mt-2">
            <span className="material-symbols-outlined text-xl">logout</span>
            Sign Out
          </button>
        </div>
      </aside>

      {/* Mobile bottom nav */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-surface-container-low border-t border-outline-variant/10 flex">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex-1 flex flex-col items-center py-3 text-xs transition-colors ${
                isActive ? 'text-primary-container' : 'text-on-surface-variant'
              }`
            }
          >
            <span className="material-symbols-outlined text-xl mb-1">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
        <button onClick={() => setMobileOpen(!mobileOpen)} className="flex-1 flex flex-col items-center py-3 text-xs text-on-surface-variant">
          <span className="material-symbols-outlined text-xl mb-1">menu</span>
          More
        </button>
      </div>

      {/* Mobile menu overlay */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-40 bg-black/60" onClick={() => setMobileOpen(false)}>
          <div className="absolute bottom-16 left-4 right-4 bg-surface-container rounded-obsidian p-4 ghost-border" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-secondary-container flex items-center justify-center font-semibold text-on-secondary">
                {user?.name?.charAt(0) || 'U'}
              </div>
              <div>
                <p className="text-sm text-on-surface">{user?.name}</p>
                <p className="text-xs text-on-surface-variant">{user?.phone}</p>
              </div>
            </div>
            <button onClick={handleLogout} className="w-full text-left flex items-center gap-3 px-3 py-2.5 rounded-obsidian text-sm text-error hover:bg-error-container/10">
              <span className="material-symbols-outlined text-lg">logout</span>
              Sign Out
            </button>
          </div>
        </div>
      )}

      {/* Main content */}
      <main className="flex-1 min-h-screen pb-20 md:pb-0">
        <Outlet />
      </main>
    </div>
  );
}
