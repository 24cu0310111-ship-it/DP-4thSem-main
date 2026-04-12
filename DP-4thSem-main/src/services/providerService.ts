import type { ServiceProvider, ComplaintCategory } from '../types';
import api from './api';

const MOCK_PROVIDERS: ServiceProvider[] = [
  {
    id: 'p1', platform: 'urban_company', name: 'QuickFix Plumbing', service_types: ['plumbing', 'water'],
    rating: 4.8, reviews_count: 234, price_range: '$$', service_areas: ['122001', '122002'],
    availability_status: 'available', avg_response_time: 45, is_active: true,
    deep_link_template: 'https://urbancompany.com/booking/plumbing',
    created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'p2', platform: 'urban_company', name: 'SparkPro Electricals', service_types: ['electricity'],
    rating: 4.6, reviews_count: 189, price_range: '$$', service_areas: ['122001'],
    availability_status: 'available', avg_response_time: 30, is_active: true,
    deep_link_template: 'https://urbancompany.com/booking/electrical',
    created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'p3', platform: 'taskrabbit', name: 'HandyMan Heroes', service_types: ['maintenance', 'plumbing', 'electricity'],
    rating: 4.3, reviews_count: 156, price_range: '$', service_areas: ['122001', '122002', '122003'],
    availability_status: 'available', avg_response_time: 60, is_active: true,
    deep_link_template: 'https://taskrabbit.com/book/handyman',
    created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'p4', platform: 'handy', name: 'ArcticBreeze HVAC', service_types: ['hvac'],
    rating: 4.9, reviews_count: 312, price_range: '$$$', service_areas: ['122001', '122002'],
    availability_status: 'busy', avg_response_time: 120, is_active: true,
    deep_link_template: 'https://handy.com/book/hvac',
    created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'p5', platform: 'local', name: 'Sharma Security Solutions', service_types: ['security'],
    rating: 4.5, reviews_count: 89, price_range: '$$', service_areas: ['122001'],
    availability_status: 'available', avg_response_time: 20, is_active: true,
    created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'p6', platform: 'local', name: 'CleanSweep Sanitation', service_types: ['sanitation'],
    rating: 4.1, reviews_count: 67, price_range: '$', service_areas: ['122001', '122002'],
    availability_status: 'available', avg_response_time: 90, is_active: true,
    created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 'p7', platform: 'urban_company', name: 'PipeWorks Pro', service_types: ['plumbing', 'water'],
    rating: 4.7, reviews_count: 198, price_range: '$$$', service_areas: ['122001'],
    availability_status: 'available', avg_response_time: 35, is_active: true,
    deep_link_template: 'https://urbancompany.com/booking/plumbing-pro',
    created_at: '2024-01-01T00:00:00Z', updated_at: '2024-01-01T00:00:00Z',
  },
];

const USE_MOCK = false;

export const providerService = {
  async getProviders(filters?: {
    category?: ComplaintCategory;
    area?: string;
    platform?: string;
    min_rating?: number;
  }): Promise<ServiceProvider[]> {
    if (USE_MOCK) {
      let filtered = MOCK_PROVIDERS.filter((p) => p.is_active);
      if (filters?.category) {
        filtered = filtered.filter((p) => p.service_types.includes(filters.category!));
      }
      if (filters?.area) {
        filtered = filtered.filter((p) => p.service_areas.includes(filters.area!));
      }
      if (filters?.platform) {
        filtered = filtered.filter((p) => p.platform === filters.platform);
      }
      if (filters?.min_rating) {
        filtered = filtered.filter((p) => p.rating >= filters.min_rating!);
      }
      return filtered.sort((a, b) => b.rating - a.rating);
    }
    const { data } = await api.get<{ data: ServiceProvider[] }>('/providers', { params: filters });
    return data.data;
  },
};
