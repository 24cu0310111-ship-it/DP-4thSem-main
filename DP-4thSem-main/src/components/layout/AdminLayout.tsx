import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { useState } from 'react';

const NAV_ITEMS = [
  { path: '/admin/dashboard', label: 'Dashboard', icon: 'dashboard' },
  { path: '/admin/complaints', label: 'Complaints', icon: 'assignment' },
];

export default function AdminLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-surface flex">
      {/* Sidebar — desktop/tablet */}
      <aside className={`hidden md:flex flex-col bg-surface-container-low border-r border-outline-variant/10 transition-all duration-300 ${collapsed ? 'w-20' : 'w-64'}`}>
        <div className="p-6 flex items-center justify-between">
          {!collapsed && (
            <NavLink to="/" className="text-xl font-display font-bold text-on-surface hover:text-primary-container transition-colors">
              SCMS
            </NavLink>
          )}
          <button onClick={() => setCollapsed(!collapsed)} className="text-on-surface-variant hover:text-on-surface p-1.5 rounded-obsidian hover:bg-surface-container transition-all">
            <span className="material-symbols-outlined text-xl">{collapsed ? 'menu_open' : 'menu'}</span>
          </button>
        </div>

        {!collapsed && <p className="px-6 text-xs text-on-surface-variant label-caps mb-4">Admin Console</p>}

        <nav className="flex-1 px-3 space-y-1">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/admin/complaints'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-obsidian text-sm font-body transition-all duration-200 ${
                  isActive
                    ? 'bg-primary-container/15 text-primary-container'
                    : 'text-on-surface-variant hover:bg-surface-container hover:text-on-surface'
                } ${collapsed ? 'justify-center' : ''}`
              }
              title={collapsed ? item.label : undefined}
            >
              <span className="material-symbols-outlined text-xl">{item.icon}</span>
              {!collapsed && item.label}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-outline-variant/10 p-4">
          {!collapsed && (
            <div className="flex items-center gap-3 px-2 py-2 mb-2">
              <div className="w-8 h-8 rounded-full bg-primary-container flex items-center justify-center text-sm font-semibold text-on-primary">
                {user?.name?.charAt(0) || 'A'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-on-surface truncate">{user?.name || 'Admin'}</p>
                <p className="text-xs label-caps text-tertiary">Admin</p>
              </div>
            </div>
          )}
          <button onClick={handleLogout} className={`flex items-center gap-3 px-4 py-2.5 rounded-obsidian text-sm text-error hover:bg-error-container/10 transition-all w-full ${collapsed ? 'justify-center' : ''}`}>
            <span className="material-symbols-outlined text-xl">logout</span>
            {!collapsed && 'Sign Out'}
          </button>
        </div>
      </aside>

      {/* Mobile top bar */}
      <div className="md:hidden fixed top-0 left-0 right-0 z-50 bg-surface-container-low border-b border-outline-variant/10 flex items-center justify-between px-4 py-3">
        <NavLink to="/" className="text-lg font-display font-bold text-on-surface">SCMS</NavLink>
        <button onClick={() => setMobileOpen(!mobileOpen)} className="text-on-surface-variant">
          <span className="material-symbols-outlined">{mobileOpen ? 'close' : 'menu'}</span>
        </button>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-40 bg-black/60" onClick={() => setMobileOpen(false)}>
          <div className="absolute top-14 left-0 bottom-0 w-72 bg-surface-container-low p-6" onClick={(e) => e.stopPropagation()}>
            <nav className="space-y-1 mb-8">
              {NAV_ITEMS.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileOpen(false)}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-4 py-3 rounded-obsidian text-sm transition-all ${
                      isActive ? 'bg-primary-container/15 text-primary-container' : 'text-on-surface-variant hover:bg-surface-container'
                    }`
                  }
                >
                  <span className="material-symbols-outlined text-xl">{item.icon}</span>
                  {item.label}
                </NavLink>
              ))}
            </nav>
            <button onClick={handleLogout} className="flex items-center gap-3 px-4 py-3 rounded-obsidian text-sm text-error hover:bg-error-container/10 w-full">
              <span className="material-symbols-outlined text-xl">logout</span>
              Sign Out
            </button>
          </div>
        </div>
      )}

      {/* Main content */}
      <main className="flex-1 min-h-screen pt-14 md:pt-0">
        <Outlet />
      </main>
    </div>
  );
}
