import type {
  Complaint,
  PaginatedResponse,
  TimelineEvent,
  ComplaintCategory,
  PriorityLevel,
  ComplaintStatus,
} from '../types';
import api from './api';

// ===== Mock Complaints =====
const MOCK_COMPLAINTS: Complaint[] = [
  {
    id: '550e8400-e29b-41d4-a716-446655440001',
    complaint_id: 'CM-20240115-0001',
    user_id: '550e8400-e29b-41d4-a716-446655440000',
    user: { name: 'Sarah Chen', phone: '+919876543210', address: { flat_no: 'A-101', building: 'Skyview Towers', area: 'Sector 15', city: 'Gurgaon', pincode: '122001' } },
    category: 'plumbing',
    subcategory: 'pipe_leak',
    description: 'Water pipe leaking in kitchen, water spreading across the floor rapidly.',
    location: 'Kitchen sink area',
    priority_level: 'critical',
    priority_score: 92.5,
    priority_reasoning: 'Active water leak with flooding risk, affects daily living and may cause property damage.',
    status: 'in_progress',
    media_urls: [],
    created_at: '2024-01-15T11:00:00Z',
    updated_at: '2024-01-15T14:30:00Z',
    estimated_resolution_time: '2024-01-15T18:00:00Z',
  },
  {
    id: '550e8400-e29b-41d4-a716-446655440002',
    complaint_id: 'CM-20240115-0002',
    user_id: '550e8400-e29b-41d4-a716-446655440000',
    user: { name: 'Sarah Chen', phone: '+919876543210', address: { flat_no: 'A-101', building: 'Skyview Towers', area: 'Sector 15', city: 'Gurgaon', pincode: '122001' } },
    category: 'electricity',
    subcategory: 'power_outage',
    description: 'Complete power outage in flat since morning. No electricity in any room.',
    location: 'Entire flat A-101',
    priority_level: 'high',
    priority_score: 78.5,
    priority_reasoning: 'Complete power loss affecting all appliances and lighting.',
    status: 'open',
    media_urls: [],
    created_at: '2024-01-16T08:00:00Z',
    updated_at: '2024-01-16T08:00:00Z',
  },
  {
    id: '550e8400-e29b-41d4-a716-446655440003',
    complaint_id: 'CM-20240114-0003',
    user_id: '550e8400-e29b-41d4-a716-446655440000',
    user: { name: 'Sarah Chen', phone: '+919876543210', address: { flat_no: 'A-101', building: 'Skyview Towers', area: 'Sector 15', city: 'Gurgaon', pincode: '122001' } },
    category: 'maintenance',
    subcategory: 'paint_peeling',
    description: 'Paint peeling off the bathroom ceiling due to moisture.',
    location: 'Master bathroom ceiling',
    priority_level: 'low',
    priority_score: 25.0,
    priority_reasoning: 'Cosmetic issue, no immediate safety or functional impact.',
    status: 'resolved',
    media_urls: [],
    created_at: '2024-01-14T09:00:00Z',
    updated_at: '2024-01-15T16:00:00Z',
    actual_resolution_time: '2024-01-15T16:00:00Z',
    user_satisfaction: 4,
  },
  {
    id: '550e8400-e29b-41d4-a716-446655440004',
    complaint_id: 'CM-20240116-0004',
    user_id: '550e8400-e29b-41d4-a716-446655440010',
    user: { name: 'Raj Patel', phone: '+919876543211', address: { flat_no: 'B-204', building: 'Skyview Towers', area: 'Sector 15', city: 'Gurgaon', pincode: '122001' } },
    category: 'water',
    subcategory: 'low_pressure',
    description: 'Very low water pressure on 2nd floor since yesterday.',
    location: 'Floor 2, all units',
    priority_level: 'medium',
    priority_score: 55.0,
    priority_reasoning: 'Affects multiple residents on the same floor.',
    status: 'assigned',
    media_urls: [],
    created_at: '2024-01-16T06:30:00Z',
    updated_at: '2024-01-16T10:00:00Z',
  },
  {
    id: '550e8400-e29b-41d4-a716-446655440005',
    complaint_id: 'CM-20240116-0005',
    user_id: '550e8400-e29b-41d4-a716-446655440011',
    user: { name: 'Elena Rodriguez', phone: '+919876543212', address: { flat_no: 'C-302', building: 'Central Mall', area: 'Sector 20', city: 'Gurgaon', pincode: '122002' } },
    category: 'hvac',
    subcategory: 'ac_malfunction',
    description: 'Central AC not cooling in the food court area. Temperature rising.',
    location: 'Food Court, Level 3',
    priority_level: 'high',
    priority_score: 82.0,
    priority_reasoning: 'Affects commercial space with high foot traffic, potential health concern.',
    status: 'open',
    media_urls: [],
    created_at: '2024-01-16T12:00:00Z',
    updated_at: '2024-01-16T12:00:00Z',
  },
  {
    id: '550e8400-e29b-41d4-a716-446655440006',
    complaint_id: 'CM-20240116-0006',
    user_id: '550e8400-e29b-41d4-a716-446655440012',
    user: { name: 'Amit Sharma', phone: '+919876543213', address: { flat_no: 'D-501', building: 'Elite Estates', area: 'Sector 10', city: 'Gurgaon', pincode: '122001' } },
    category: 'security',
    subcategory: 'broken_lock',
    description: 'Main entrance gate lock is broken. Security compromised.',
    location: 'Main entrance gate',
    priority_level: 'critical',
    priority_score: 95.0,
    priority_reasoning: 'Security breach risk, affects all residents.',
    status: 'in_progress',
    media_urls: [],
    created_at: '2024-01-16T07:00:00Z',
    updated_at: '2024-01-16T08:30:00Z',
  },
];

const MOCK_TIMELINE: TimelineEvent[] = [
  {
    id: '1',
    complaint_id: 'CM-20240115-0001',
    event_type: 'created',
    event_data: {},
    created_at: '2024-01-15T11:00:00Z',
  },
  {
    id: '2',
    complaint_id: 'CM-20240115-0001',
    event_type: 'prioritized',
    event_data: { priority_level: 'critical', priority_score: 92.5, reasoning: 'Active water leak with flooding risk' },
    created_at: '2024-01-15T11:00:05Z',
  },
  {
    id: '3',
    complaint_id: 'CM-20240115-0001',
    event_type: 'assigned',
    event_data: { provider_name: 'QuickFix Plumbing', platform: 'urban_company' },
    performed_by_name: 'Marcus Thorne',
    created_at: '2024-01-15T12:30:00Z',
  },
  {
    id: '4',
    complaint_id: 'CM-20240115-0001',
    event_type: 'status_changed',
    event_data: { previous_status: 'open', new_status: 'in_progress' },
    performed_by_name: 'Marcus Thorne',
    created_at: '2024-01-15T14:30:00Z',
  },
];

const USE_MOCK = false;

export const complaintService = {
  async getUserComplaints(
    filters?: { status?: ComplaintStatus; priority?: PriorityLevel; page?: number; limit?: number }
  ): Promise<PaginatedResponse<Complaint>> {
    if (USE_MOCK) {
      let filtered = [...MOCK_COMPLAINTS];
      if (filters?.status) filtered = filtered.filter((c) => c.status === filters.status);
      if (filters?.priority) filtered = filtered.filter((c) => c.priority_level === filters.priority);
      return {
        data: filtered,
        pagination: { page: 1, limit: 20, total: filtered.length, total_pages: 1 },
      };
    }
    const { data } = await api.get<PaginatedResponse<Complaint>>('/user/complaints', { params: filters });
    return data;
  },

  async getAdminComplaints(
    filters?: {
      priority?: string;
      status?: string;
      category?: ComplaintCategory;
      area?: string;
      page?: number;
      limit?: number;
      sort?: string;
    }
  ): Promise<PaginatedResponse<Complaint>> {
    if (USE_MOCK) {
      let filtered = [...MOCK_COMPLAINTS];
      if (filters?.category) filtered = filtered.filter((c) => c.category === filters.category);
      if (filters?.status) filtered = filtered.filter((c) => c.status === filters.status);
      return {
        data: filtered,
        pagination: { page: 1, limit: 50, total: filtered.length, total_pages: 1 },
      };
    }
    const { data } = await api.get<PaginatedResponse<Complaint>>('/admin/complaints', { params: filters });
    return data;
  },

  async getComplaint(id: string): Promise<Complaint> {
    if (USE_MOCK) {
      const found = MOCK_COMPLAINTS.find((c) => c.id === id || c.complaint_id === id);
      if (!found) throw new Error('Complaint not found');
      return found;
    }
    const { data } = await api.get<Complaint>(`/admin/complaints/${id}`);
    return data;
  },

  async getTimeline(complaintId: string): Promise<TimelineEvent[]> {
    if (USE_MOCK) {
      return MOCK_TIMELINE.filter((t) => t.complaint_id === complaintId);
    }
    const { data } = await api.get<{ timeline: TimelineEvent[] }>(`/user/complaints/${complaintId}/timeline`);
    return data.timeline;
  },
};
