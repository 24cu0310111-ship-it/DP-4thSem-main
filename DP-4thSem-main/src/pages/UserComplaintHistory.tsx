import { useState } from 'react';
import { useComplaints } from '../hooks/useComplaints';
import type { ComplaintStatus, PriorityLevel } from '../types';

const STATUS_TABS: { label: string; value: ComplaintStatus | 'all' }[] = [
  { label: 'All', value: 'all' },
  { label: 'Open', value: 'open' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Resolved', value: 'resolved' },
];

const PRIORITY_COLORS: Record<PriorityLevel, string> = {
  critical: 'bg-error/20 text-error border-error/30',
  high: 'bg-warning/20 text-warning border-warning/30',
  medium: 'bg-primary-container/20 text-primary-container border-primary-container/30',
  low: 'bg-on-surface-variant/20 text-on-surface-variant border-outline-variant/30',
};

const STATUS_COLORS: Record<string, string> = {
  open: 'bg-tertiary-container/20 text-tertiary border-tertiary-container/30',
  in_progress: 'bg-primary-container/20 text-primary-container border-primary-container/30',
  assigned: 'bg-secondary-container/20 text-secondary border-secondary/30',
  resolved: 'bg-success/20 text-success border-success/30',
  closed: 'bg-outline-variant/20 text-on-surface-variant border-outline-variant/30',
  escalated: 'bg-error/20 text-error border-error/30',
};

export default function UserComplaintHistory() {
  const [activeTab, setActiveTab] = useState<ComplaintStatus | 'all'>('all');
  const { complaints, isLoading } = useComplaints('user');

  const filtered = activeTab === 'all'
    ? complaints
    : complaints.filter((c) => c.status === activeTab);

  return (
    <div className="p-6 lg:p-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl lg:text-3xl font-headline font-bold text-on-surface mb-2">
          Complaint History
        </h1>
        <p className="text-on-surface-variant text-sm">
          Track and manage your submitted complaints
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-surface-container-low rounded-obsidian p-1 mb-6 overflow-x-auto">
        {STATUS_TABS.map((tab) => (
          <button
            key={tab.value}
            onClick={() => setActiveTab(tab.value)}
            className={`px-4 py-2 rounded-[6px] text-sm font-label font-semibold whitespace-nowrap transition-all ${
              activeTab === tab.value
                ? 'bg-primary-container text-on-primary shadow-primary-glow'
                : 'text-on-surface-variant hover:text-on-surface'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Loading */}
      {isLoading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-primary-container border-t-transparent rounded-full animate-spin" />
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-20">
          <span className="material-symbols-outlined text-5xl text-outline mb-4 block">inbox</span>
          <p className="text-on-surface-variant">No complaints found</p>
        </div>
      ) : (
        <>
          {/* Desktop Table */}
          <div className="hidden lg:block overflow-hidden rounded-obsidian ghost-border">
            <table className="w-full">
              <thead>
                <tr className="bg-surface-container-low">
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">ID</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Category</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Description</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Priority</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Status</th>
                  <th className="text-left px-6 py-4 label-caps text-on-surface-variant">Date</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((complaint) => (
                  <tr key={complaint.id} className="border-t border-outline-variant/10 hover:bg-surface-container/50 transition-colors">
                    <td className="px-6 py-4 text-sm font-body text-primary-container font-medium">{complaint.complaint_id}</td>
                    <td className="px-6 py-4 text-sm font-body text-on-surface capitalize">{complaint.category}</td>
                    <td className="px-6 py-4 text-sm font-body text-on-surface-variant max-w-xs truncate">{complaint.description}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-label font-semibold uppercase border ${PRIORITY_COLORS[complaint.priority_level]}`}>
                        {complaint.priority_level}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-label font-semibold uppercase border ${STATUS_COLORS[complaint.status]}`}>
                        {complaint.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-on-surface-variant">{new Date(complaint.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile/Tablet Cards */}
          <div className="lg:hidden grid grid-cols-1 md:grid-cols-2 gap-4">
            {filtered.map((complaint) => (
              <div key={complaint.id} className="bg-surface-container rounded-obsidian p-5 ghost-border card-interactive">
                <div className="flex items-start justify-between mb-3">
                  <span className="text-sm font-body text-primary-container font-medium">{complaint.complaint_id}</span>
                  <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-label font-semibold uppercase border ${PRIORITY_COLORS[complaint.priority_level]}`}>
                    {complaint.priority_level}
                  </span>
                </div>
                <p className="text-sm text-on-surface mb-2 line-clamp-2">{complaint.description}</p>
                <div className="flex items-center justify-between">
                  <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-label uppercase border ${STATUS_COLORS[complaint.status]}`}>
                    {complaint.status.replace('_', ' ')}
                  </span>
                  <span className="text-xs text-on-surface-variant">{new Date(complaint.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
