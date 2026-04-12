import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState<'user' | 'admin'>('user');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const loginPhone = activeTab === 'admin' ? 'admin' : phone;
      const user = await login({ phone: loginPhone, password });

      const from = (location.state as { from?: { pathname: string } })?.from?.pathname;
      if (from) {
        navigate(from, { replace: true });
      } else {
        navigate(
          user.role === 'admin' || user.role === 'super_admin'
            ? '/admin/dashboard'
            : '/user/history',
          { replace: true }
        );
      }
    } catch {
      setError('Invalid credentials. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface flex">
      {/* Left decorative panel — desktop only */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden items-center justify-center bg-surface-container-low">
        {/* Gradient orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-container/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-1/3 right-1/4 w-72 h-72 bg-tertiary-container/10 rounded-full blur-[100px]" />
        <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-secondary/5 rounded-full blur-[80px]" />

        <div className="relative z-10 max-w-md px-8 text-center">
          <h1 className="text-5xl font-display font-bold text-on-surface mb-4 display-text">
            SCMS
          </h1>
          <p className="text-xl text-on-surface-variant font-body leading-relaxed">
            Smart Complaint Management System
          </p>
          <div className="mt-8 flex items-center justify-center gap-2">
            <span className="w-2 h-2 rounded-full bg-tertiary-container intelligence-glow" />
            <span className="label-caps text-tertiary">Kinetic Intelligence</span>
          </div>
        </div>
      </div>

      {/* Right login form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="lg:hidden text-center mb-10">
            <h1 className="text-3xl font-display font-bold text-on-surface">SCMS</h1>
            <p className="text-sm text-on-surface-variant mt-1">Smart Complaint Management</p>
          </div>

          {/* Card */}
          <div className="bg-surface-container rounded-obsidian p-8 ghost-border">
            <h2 className="text-2xl font-headline font-semibold text-on-surface mb-2">
              Welcome back
            </h2>
            <p className="text-on-surface-variant text-sm mb-8">
              Sign in to your account to continue
            </p>

            {/* Tabs */}
            <div className="flex rounded-obsidian bg-surface-container-low p-1 mb-8">
              <button
                onClick={() => { setActiveTab('user'); setError(''); }}
                className={`flex-1 py-2.5 px-4 rounded-[6px] text-sm font-label font-semibold uppercase tracking-wider transition-all duration-200 ${
                  activeTab === 'user'
                    ? 'bg-primary-container text-on-primary shadow-primary-glow'
                    : 'text-on-surface-variant hover:text-on-surface'
                }`}
              >
                User
              </button>
              <button
                onClick={() => { setActiveTab('admin'); setError(''); }}
                className={`flex-1 py-2.5 px-4 rounded-[6px] text-sm font-label font-semibold uppercase tracking-wider transition-all duration-200 ${
                  activeTab === 'admin'
                    ? 'bg-primary-container text-on-primary shadow-primary-glow'
                    : 'text-on-surface-variant hover:text-on-surface'
                }`}
              >
                Admin
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              {activeTab === 'user' ? (
                <div>
                  <label className="label-caps text-on-surface-variant block mb-2">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="+91 98765 43210"
                    className="input-obsidian w-full px-4 py-3 rounded-obsidian text-sm"
                    required
                  />
                </div>
              ) : (
                <div>
                  <label className="label-caps text-on-surface-variant block mb-2">
                    Admin ID
                  </label>
                  <input
                    type="text"
                    value="admin"
                    disabled
                    className="input-obsidian w-full px-4 py-3 rounded-obsidian text-sm opacity-60"
                  />
                </div>
              )}

              <div>
                <label className="label-caps text-on-surface-variant block mb-2">
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="input-obsidian w-full px-4 py-3 rounded-obsidian text-sm"
                  required
                />
              </div>

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center gap-2 text-on-surface-variant cursor-pointer">
                  <input type="checkbox" className="rounded border-outline-variant bg-surface-container-low accent-primary-container" />
                  Remember me
                </label>
                <button type="button" className="text-primary-container hover:text-primary transition-colors">
                  Forgot password?
                </button>
              </div>

              {error && (
                <div className="bg-error-container/20 border border-error/20 rounded-obsidian p-3 text-error text-sm">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full gradient-primary text-on-primary font-label font-semibold uppercase tracking-wider py-3.5 rounded-obsidian transition-all duration-200 hover:scale-[1.02] hover:shadow-primary-glow disabled:opacity-50 disabled:hover:scale-100"
              >
                {isSubmitting ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="w-4 h-4 border-2 border-on-primary border-t-transparent rounded-full animate-spin" />
                    Signing in...
                  </span>
                ) : (
                  'Sign In'
                )}
              </button>
            </form>

            {/* Divider */}
            <div className="flex items-center gap-4 my-6">
              <div className="flex-1 h-px bg-outline-variant/20" />
              <span className="label-caps text-outline text-xs">or continue with</span>
              <div className="flex-1 h-px bg-outline-variant/20" />
            </div>

            {/* Social login */}
            <div className="grid grid-cols-2 gap-3">
              <button className="flex items-center justify-center gap-2 py-2.5 rounded-obsidian ghost-border text-on-surface-variant text-sm hover:bg-surface-container-high transition-all">
                <span className="material-symbols-outlined text-lg">mail</span>
                Google
              </button>
              <button className="flex items-center justify-center gap-2 py-2.5 rounded-obsidian ghost-border text-on-surface-variant text-sm hover:bg-surface-container-high transition-all">
                <span className="material-symbols-outlined text-lg">phone_iphone</span>
                OTP
              </button>
            </div>

            {/* Demo credentials */}
            <div className="mt-6 p-3 bg-surface-container-low rounded-obsidian">
              <p className="label-caps text-tertiary text-xs mb-2">Demo Credentials</p>
              <div className="space-y-1 text-xs text-on-surface-variant">
                <p><span className="text-on-surface">User:</span> +919876543210 / user123</p>
                <p><span className="text-on-surface">Admin:</span> admin / admin123</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
