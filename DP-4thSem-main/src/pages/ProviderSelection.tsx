import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { complaintService } from '../services/complaintService';
import { useProviders } from '../hooks/useProviders';
import type { Complaint, PriorityLevel, Platform } from '../types';

const PRIORITY_COLORS: Record<PriorityLevel, string> = {
  critical: 'bg-error/20 text-error',
  high: 'bg-warning/20 text-warning',
  medium: 'bg-primary-container/20 text-primary-container',
  low: 'bg-outline-variant/20 text-on-surface-variant',
};

const PLATFORM_COLORS: Record<Platform, { bg: string; text: string }> = {
  urban_company: { bg: 'bg-primary-container/20', text: 'text-primary-container' },
  taskrabbit: { bg: 'bg-secondary-container/20', text: 'text-secondary' },
  handy: { bg: 'bg-tertiary-container/20', text: 'text-tertiary' },
  local: { bg: 'bg-on-surface-variant/10', text: 'text-on-surface-variant' },
};

export default function ProviderSelection() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [complaint, setComplaint] = useState<Complaint | null>(null);
  const [loading, setLoading] = useState(true);
  const [platformFilter, setPlatformFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'rating' | 'price' | 'response'>('rating');

  const { providers, isLoading: providersLoading } = useProviders(
    complaint?.category,
    complaint?.user?.address?.pincode
  );

  useEffect(() => {
    if (!id) return;
    complaintService.getComplaint(id).then((c) => {
      setComplaint(c);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  const filteredProviders = providers
    .filter((p) => platformFilter === 'all' || p.platform === platformFilter)
    .sort((a, b) => {
      if (sortBy === 'rating') return b.rating - a.rating;
      if (sortBy === 'response') return a.avg_response_time - b.avg_response_time;
      const priceOrder = { '$': 1, '$$': 2, '$$$': 3 };
      return priceOrder[a.price_range] - priceOrder[b.price_range];
    });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-8 h-8 border-2 border-primary-container border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!complaint) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <span className="material-symbols-outlined text-5xl text-outline">error_outline</span>
        <p className="text-on-surface-variant">Complaint not found</p>
        <button onClick={() => navigate('/admin/complaints')} className="text-primary-container hover:underline text-sm">
          ← Back to Console
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 lg:p-8">
      {/* Back button */}
      <button
        onClick={() => navigate('/admin/complaints')}
        className="flex items-center gap-2 text-on-surface-variant hover:text-on-surface text-sm mb-6 transition-colors"
      >
        <span className="material-symbols-outlined text-lg">arrow_back</span>
        Back to Console
      </button>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Left — Complaint Summary */}
        <div className="lg:w-[360px] flex-shrink-0 space-y-4">
          {/* Complaint Card */}
          <div className="bg-surface-container rounded-obsidian p-6 ghost-border">
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm text-primary-container font-medium">{complaint.complaint_id}</p>
                <h2 className="text-lg font-headline font-semibold text-on-surface mt-1 capitalize">{complaint.category} Issue</h2>
              </div>
              <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-label uppercase ${PRIORITY_COLORS[complaint.priority_level]}`}>
                {complaint.priority_level}
              </span>
            </div>

            <p className="text-sm text-on-surface-variant mb-4 leading-relaxed">{complaint.description}</p>

            <div className="space-y-3 text-sm">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-lg text-outline">person</span>
                <span className="text-on-surface">{complaint.user?.name}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-lg text-outline">location_on</span>
                <span className="text-on-surface-variant">{complaint.location}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-lg text-outline">schedule</span>
                <span className="text-on-surface-variant">{new Date(complaint.created_at).toLocaleString()}</span>
              </div>
            </div>

            {complaint.priority_reasoning && (
              <div className="mt-4 p-3 bg-surface-container-low rounded-obsidian">
                <p className="label-caps text-tertiary text-xs mb-1">AI Analysis</p>
                <p className="text-xs text-on-surface-variant leading-relaxed">{complaint.priority_reasoning}</p>
              </div>
            )}
          </div>

          {/* Filters */}
          <div className="bg-surface-container rounded-obsidian p-5 ghost-border">
            <p className="label-caps text-on-surface-variant mb-3">Filter Providers</p>
            <div className="space-y-3">
              <select
                value={platformFilter}
                onChange={(e) => setPlatformFilter(e.target.value)}
                className="input-obsidian w-full px-3 py-2.5 rounded-obsidian text-sm"
              >
                <option value="all">All Platforms</option>
                <option value="urban_company">Urban Company</option>
                <option value="taskrabbit">TaskRabbit</option>
                <option value="handy">Handy</option>
                <option value="local">Local</option>
              </select>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
                className="input-obsidian w-full px-3 py-2.5 rounded-obsidian text-sm"
              >
                <option value="rating">Sort by Rating</option>
                <option value="price">Sort by Price</option>
                <option value="response">Sort by Response Time</option>
              </select>
            </div>
          </div>
        </div>

        {/* Right — Provider Cards */}
        <div className="flex-1">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-headline font-semibold text-on-surface">
              Available Providers
              <span className="text-sm text-on-surface-variant font-body font-normal ml-2">({filteredProviders.length})</span>
            </h3>
          </div>

          {providersLoading ? (
            <div className="flex items-center justify-center py-20">
              <div className="w-8 h-8 border-2 border-primary-container border-t-transparent rounded-full animate-spin" />
            </div>
          ) : filteredProviders.length === 0 ? (
            <div className="text-center py-20 bg-surface-container rounded-obsidian ghost-border">
              <span className="material-symbols-outlined text-5xl text-outline mb-4 block">search_off</span>
              <p className="text-on-surface-variant">No providers found for this category</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredProviders.map((provider) => (
                <div key={provider.id} className="bg-surface-container rounded-obsidian p-5 ghost-border card-interactive">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-11 h-11 rounded-obsidian bg-surface-container-high flex items-center justify-center">
                        <span className="material-symbols-outlined text-on-surface-variant">handyman</span>
                      </div>
                      <div>
                        <p className="text-sm font-body font-medium text-on-surface">{provider.name}</p>
                        <span className={`inline-flex px-2 py-0.5 rounded-full text-[10px] font-label uppercase mt-1 ${PLATFORM_COLORS[provider.platform].bg} ${PLATFORM_COLORS[provider.platform].text}`}>
                          {provider.platform.replace('_', ' ')}
                        </span>
                      </div>
                    </div>
                    {/* Availability dot */}
                    <span className={`w-2.5 h-2.5 rounded-full ${
                      provider.availability_status === 'available' ? 'bg-success' :
                      provider.availability_status === 'busy' ? 'bg-warning' : 'bg-error'
                    }`} title={provider.availability_status} />
                  </div>

                  {/* Stats */}
                  <div className="grid grid-cols-3 gap-3 mb-4">
                    <div>
                      <p className="label-caps text-[10px] text-on-surface-variant mb-0.5">Rating</p>
                      <p className="text-sm text-on-surface font-medium flex items-center gap-1">
                        <span className="text-warning text-xs">★</span>{provider.rating}
                        <span className="text-[10px] text-outline">({provider.reviews_count})</span>
                      </p>
                    </div>
                    <div>
                      <p className="label-caps text-[10px] text-on-surface-variant mb-0.5">Price</p>
                      <p className="text-sm text-on-surface font-medium">{provider.price_range}</p>
                    </div>
                    <div>
                      <p className="label-caps text-[10px] text-on-surface-variant mb-0.5">Response</p>
                      <p className="text-sm text-on-surface font-medium">{provider.avg_response_time}m</p>
                    </div>
                  </div>

                  {/* Book button */}
                  <button
                    onClick={() => {
                      if (provider.deep_link_template) {
                        window.open(provider.deep_link_template, '_blank');
                      }
                    }}
                    className="w-full gradient-primary text-on-primary font-label font-semibold uppercase tracking-wider py-2.5 rounded-obsidian text-sm transition-all hover:scale-[1.02] hover:shadow-primary-glow"
                  >
                    Book Now
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
