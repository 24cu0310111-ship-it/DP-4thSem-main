import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { complaintService } from '../services/complaintService';
import { useComplaints } from '../hooks/useComplaints';
import type { PriorityLevel, ComplaintCategory } from '../types';

const PRIORITY_COLORS: Record<PriorityLevel, string> = {
  critical: 'bg-error/20 text-error border-error/30',
  high: 'bg-warning/20 text-warning border-warning/30',
  medium: 'bg-primary-container/20 text-primary-container border-primary-container/30',
  low: 'bg-outline-variant/20 text-on-surface-variant border-outline-variant/30',
};

const STATUS_COLORS: Record<string, string> = {
  open: 'bg-tertiary-container/20 text-tertiary border-tertiary-container/30',
  in_progress: 'bg-primary-container/20 text-primary-container border-primary-container/30',
  assigned: 'bg-secondary-container/20 text-secondary border-secondary/30',
  resolved: 'bg-success/20 text-success border-success/30',
  closed: 'bg-outline-variant/20 text-on-surface-variant border-outline-variant/30',
  escalated: 'bg-error/20 text-error border-error/30',
};

const CATEGORIES: ComplaintCategory[] = ['electricity', 'water', 'sanitation', 'hvac', 'plumbing', 'maintenance', 'security', 'other'];

export default function AdminComplaintConsole() {
  const { complaints, isLoading } = useComplaints('admin');
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [updating, setUpdating] = useState<Set<string>>(new Set());

  const handleMarkInProgress = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      setUpdating((prev) => new Set(prev).add(id));
      await complaintService.updateStatus(id, 'in_progress');
      window.location.reload(); 
    } catch (err) {
      console.error(err);
    } finally {
      setUpdating((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  };
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');

  const filtered = complaints.filter((c) => {
    const matchesSearch = c.complaint_id.toLowerCase().includes(search.toLowerCase()) ||
      c.description.toLowerCase().includes(search.toLowerCase()) ||
      c.user?.name?.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = categoryFilter === 'all' || c.category === categoryFilter;
    const matchesPriority = priorityFilter === 'all' || c.priority_level === priorityFilter;
    return matchesSearch && matchesCategory && matchesPriority;
  });

  return (
    <div className="p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl lg:text-3xl font-headline font-bold text-on-surface mb-2">Complaint Console</h1>
        <p className="text-on-surface-variant text-sm">Manage and resolve incoming complaints</p>
      </div>

      {/* Filters */}
      <div className="flex flex-col md:flex-row gap-3 mb-6">
        <div className="flex-1">
          <div className="relative">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline text-xl">search</span>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search complaints..."
              className="input-obsidian w-full pl-10 pr-4 py-3 rounded-obsidian text-sm"
            />
          </div>
        </div>
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="input-obsidian px-4 py-3 rounded-obsidian text-sm min-w-[160px]"
        >
          <option value="all">All Categories</option>
          {CATEGORIES.map((cat) => (
            <option key={cat} value={cat} className="capitalize">{cat}</option>
          ))}
        </select>
        <select
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
          className="input-obsidian px-4 py-3 rounded-obsidian text-sm min-w-[140px]"
        >
          <option value="all">All Priorities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-primary-container border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <>
          {/* Desktop Table */}
          <div className="hidden lg:block overflow-hidden rounded-obsidian ghost-border">
            <table className="w-full">
              <thead>
                <tr className="bg-surface-container-low">
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">ID</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">User</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Category</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Description</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Priority</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Status</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((c) => (
                  <tr key={c.id} className="border-t border-outline-variant/10 hover:bg-surface-container/50 transition-colors">
                    <td className="px-6 py-4 text-sm text-primary-container font-medium">{c.complaint_id}</td>
                    <td className="px-6 py-4">
                      <p className="text-sm text-on-surface">{c.user?.name || '—'}</p>
                      <p className="text-xs text-on-surface-variant flex items-center gap-1 mt-0.5">
                        <span className="material-symbols-outlined text-[12px]">location_on</span>
                        {c.location && c.location.includes(',') ? c.location : c.user?.address?.area || c.location}
                      </p>
                    </td>
                    <td className="px-6 py-4 text-sm text-on-surface capitalize">{c.category}</td>
                    <td className="px-6 py-4 text-sm text-on-surface-variant max-w-[200px] truncate" title={c.description}>{c.description}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-label uppercase border ${PRIORITY_COLORS[c.priority_level]}`}>
                        {c.priority_level === 'critical' && <span className="w-1.5 h-1.5 rounded-full bg-error animate-pulse" />}
                        {c.priority_level}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-label uppercase border ${STATUS_COLORS[c.status]}`}>
                        {c.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <button
                          onClick={() => navigate(`/admin/complaints/${c.id}/providers`)}
                          className="text-sm text-primary-container hover:text-primary font-medium transition-colors hover:underline"
                        >
                          View Details
                        </button>
                        {(c.status === 'open' || c.status === 'assigned') && (
                          <button
                            onClick={(e) => handleMarkInProgress(c.id, e)}
                            disabled={updating.has(c.id)}
                            className="bg-primary-container/10 text-primary-container text-xs px-3 py-1.5 rounded-full hover:bg-primary-container/20 transition-all font-medium disabled:opacity-50"
                          >
                            {updating.has(c.id) ? 'Updating...' : 'Start Progress'}
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile/Tablet Cards */}
          <div className="lg:hidden space-y-3">
            {filtered.map((c) => (
              <div key={c.id} className="bg-surface-container rounded-obsidian p-5 ghost-border card-interactive" onClick={() => navigate(`/admin/complaints/${c.id}/providers`)}>
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <p className="text-sm text-primary-container font-medium">{c.complaint_id}</p>
                    <p className="text-xs text-on-surface-variant">{c.user?.name} • {c.user?.address?.area}</p>
                  </div>
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-label uppercase border ${PRIORITY_COLORS[c.priority_level]}`}>
                    {c.priority_level === 'critical' && <span className="w-1.5 h-1.5 rounded-full bg-error animate-pulse" />}
                    {c.priority_level}
                  </span>
                </div>
                <p className="text-sm text-on-surface mb-3 line-clamp-2">{c.description}</p>
                <div className="flex items-center justify-between">
                  <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-label uppercase border ${STATUS_COLORS[c.status]}`}>
                    {c.status.replace('_', ' ')}
                  </span>
                  <span className="text-xs text-primary-container font-medium">View Details →</span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
