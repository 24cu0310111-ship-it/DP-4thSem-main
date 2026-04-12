import type { DashboardAnalytics } from '../types';
import api from './api';

const MOCK_ANALYTICS: DashboardAnalytics = {
  total_open: 45,
  critical_count: 3,
  high_count: 12,
  avg_resolution_time_hours: 18.5,
  satisfaction_score: 4.2,
  complaints_by_category: {
    electricity: 15,
    water: 12,
    plumbing: 10,
    sanitation: 4,
    hvac: 6,
    maintenance: 5,
    security: 3,
    other: 2,
  },
  complaints_by_priority: {
    critical: 3,
    high: 12,
    medium: 20,
    low: 10,
  },
  trend: {
    this_week: 45,
    last_week: 38,
    change_percent: 18.4,
  },
};

const USE_MOCK = false;

export const adminService = {
  async getAnalytics(): Promise<DashboardAnalytics> {
    if (USE_MOCK) return MOCK_ANALYTICS;
    const { data } = await api.get<DashboardAnalytics>('/admin/analytics/overview');
    return data;
  },
};
