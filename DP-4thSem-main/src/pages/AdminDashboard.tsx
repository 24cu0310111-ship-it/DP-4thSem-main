import { useState, useEffect } from 'react';
import { adminService } from '../services/adminService';
import { useComplaints } from '../hooks/useComplaints';
import type { DashboardAnalytics, PriorityLevel } from '../types';

const PRIORITY_COLORS: Record<PriorityLevel, string> = {
  critical: 'bg-error/20 text-error',
  high: 'bg-warning/20 text-warning',
  medium: 'bg-primary-container/20 text-primary-container',
  low: 'bg-outline-variant/20 text-on-surface-variant',
};

export default function AdminDashboard() {
  const [analytics, setAnalytics] = useState<DashboardAnalytics | null>(null);
  const { complaints } = useComplaints('admin');

  useEffect(() => {
    adminService.getAnalytics().then(setAnalytics);
  }, []);

  if (!analytics) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-8 h-8 border-2 border-primary-container border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const statCards = [
    { label: 'Total Open', value: analytics.total_open, icon: 'assignment', color: 'text-primary-container', glow: false },
    { label: 'Critical', value: analytics.critical_count, icon: 'warning', color: 'text-error', glow: true },
    { label: 'Avg Resolution', value: `${analytics.avg_resolution_time_hours}h`, icon: 'schedule', color: 'text-tertiary', glow: false },
    { label: 'Satisfaction', value: `${analytics.satisfaction_score}/5`, icon: 'sentiment_satisfied', color: 'text-success', glow: false },
  ];

  return (
    <div className="p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl lg:text-3xl font-headline font-bold text-on-surface mb-2">Dashboard</h1>
        <p className="text-on-surface-variant text-sm">Overview of complaint management metrics</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
        {statCards.map((stat) => (
          <div
            key={stat.label}
            className={`bg-surface-container rounded-obsidian p-6 ghost-border card-interactive ${stat.glow ? 'intelligence-glow' : ''}`}
          >
            <div className="flex items-start justify-between mb-4">
              <span className={`material-symbols-outlined text-2xl ${stat.color}`}>{stat.icon}</span>
              {stat.label === 'Total Open' && (
                <span className={`text-xs label-caps ${analytics.trend.change_percent > 0 ? 'text-error' : 'text-success'}`}>
                  {analytics.trend.change_percent > 0 ? '↑' : '↓'}{Math.abs(analytics.trend.change_percent)}%
                </span>
              )}
            </div>
            <p className="text-3xl font-display font-bold text-on-surface mb-1">{stat.value}</p>
            <p className="label-caps text-on-surface-variant">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Category Breakdown */}
        <div className="bg-surface-container rounded-obsidian p-6 ghost-border">
          <h3 className="text-lg font-headline font-semibold text-on-surface mb-6">By Category</h3>
          <div className="space-y-3">
            {Object.entries(analytics.complaints_by_category).map(([cat, count]) => {
              const max = Math.max(...Object.values(analytics.complaints_by_category));
              return (
                <div key={cat} className="flex items-center gap-3">
                  <span className="text-sm text-on-surface-variant capitalize w-24 truncate">{cat}</span>
                  <div className="flex-1 h-2.5 bg-surface-container-high rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-primary-container to-tertiary-container rounded-full transition-all duration-700"
                      style={{ width: `${(count / max) * 100}%` }}
                    />
                  </div>
                  <span className="text-sm text-on-surface font-medium w-8 text-right">{count}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Priority Distribution */}
        <div className="bg-surface-container rounded-obsidian p-6 ghost-border">
          <h3 className="text-lg font-headline font-semibold text-on-surface mb-6">By Priority</h3>
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(analytics.complaints_by_priority).map(([priority, count]) => (
              <div key={priority} className={`rounded-obsidian p-4 ${PRIORITY_COLORS[priority as PriorityLevel]}`}>
                <p className="text-2xl font-display font-bold mb-1">{count}</p>
                <p className="label-caps text-xs capitalize">{priority}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Complaints Table */}
      <div className="bg-surface-container rounded-obsidian ghost-border overflow-hidden">
        <div className="px-6 py-4 border-b border-outline-variant/10">
          <h3 className="text-lg font-headline font-semibold text-on-surface">Recent Complaints</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-surface-container-low">
                <th className="text-left px-6 py-3 label-caps text-on-surface-variant">ID</th>
                <th className="text-left px-6 py-3 label-caps text-on-surface-variant">User</th>
                <th className="text-left px-6 py-3 label-caps text-on-surface-variant hidden md:table-cell">Category</th>
                <th className="text-left px-6 py-3 label-caps text-on-surface-variant">Priority</th>
                <th className="text-left px-6 py-3 label-caps text-on-surface-variant hidden lg:table-cell">Status</th>
              </tr>
            </thead>
            <tbody>
              {complaints.slice(0, 5).map((c) => (
                <tr key={c.id} className="border-t border-outline-variant/10 hover:bg-surface-container-high/30 transition-colors">
                  <td className="px-6 py-3 text-sm text-primary-container font-medium">{c.complaint_id}</td>
                  <td className="px-6 py-3 text-sm text-on-surface">{c.user?.name || '—'}</td>
                  <td className="px-6 py-3 text-sm text-on-surface-variant capitalize hidden md:table-cell">{c.category}</td>
                  <td className="px-6 py-3">
                    <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-label uppercase ${PRIORITY_COLORS[c.priority_level]}`}>
                      {c.priority_level}
                    </span>
                  </td>
                  <td className="px-6 py-3 text-sm text-on-surface-variant capitalize hidden lg:table-cell">{c.status.replace('_', ' ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
