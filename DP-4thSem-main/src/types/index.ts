// ===== User Types =====
export type UserRole = 'user' | 'admin' | 'super_admin';

export interface UserAddress {
  flat_no: string;
  building: string;
  street?: string;
  area: string;
  city: string;
  state?: string;
  pincode: string;
  coordinates?: { lat: number; lng: number };
}

export interface User {
  id: string;
  phone: string;
  email?: string;
  name: string;
  role: UserRole;
  address: UserAddress;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// ===== Auth Types =====
export interface LoginRequest {
  phone: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: Pick<User, 'id' | 'name' | 'role'>;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// ===== Complaint Types =====
export type ComplaintCategory =
  | 'electricity'
  | 'water'
  | 'sanitation'
  | 'hvac'
  | 'plumbing'
  | 'maintenance'
  | 'security'
  | 'other';

export type PriorityLevel = 'critical' | 'high' | 'medium' | 'low';

export type ComplaintStatus =
  | 'open'
  | 'in_progress'
  | 'assigned'
  | 'resolved'
  | 'closed'
  | 'escalated';

export interface AIAnalysis {
  category_confidence: number;
  subcategory_confidence?: number;
  extracted_entities: Record<string, string>;
  urgency_keywords: string[];
  affected_users: 'single' | 'multiple' | 'building';
  safety_risk: boolean;
  detected_language: string;
  sentiment_score: number;
  media_analysis?: string;
}

export interface Complaint {
  id: string;
  complaint_id: string;
  user_id: string;
  user?: Pick<User, 'name' | 'phone' | 'email' | 'address'>;
  category: ComplaintCategory;
  subcategory: string;
  description: string;
  location: string;
  priority_level: PriorityLevel;
  priority_score: number;
  priority_reasoning?: string;
  status: ComplaintStatus;
  ai_analysis?: AIAnalysis;
  media_urls: string[];
  assigned_provider?: ServiceProvider;
  assigned_provider_id?: string;
  assigned_admin_id?: string;
  estimated_resolution_time?: string;
  actual_resolution_time?: string;
  user_satisfaction?: number;
  created_at: string;
  updated_at: string;
}

// ===== Timeline Types =====
export type TimelineEventType =
  | 'created'
  | 'prioritized'
  | 'assigned'
  | 'status_changed'
  | 'provider_booked'
  | 'resolved'
  | 'escalated'
  | 'commented';

export interface TimelineEvent {
  id: string;
  complaint_id: string;
  event_type: TimelineEventType;
  event_data: Record<string, unknown>;
  performed_by?: string;
  performed_by_name?: string;
  created_at: string;
}

// ===== Service Provider Types =====
export type Platform = 'urban_company' | 'taskrabbit' | 'handy' | 'local';
export type PriceRange = '$' | '$$' | '$$$';
export type AvailabilityStatus = 'available' | 'busy' | 'unavailable';

export interface ServiceProvider {
  id: string;
  platform: Platform;
  platform_provider_id?: string;
  name: string;
  service_types: string[];
  rating: number;
  reviews_count: number;
  price_range: PriceRange;
  service_areas: string[];
  availability_status: AvailabilityStatus;
  avg_response_time: number; // minutes
  deep_link_template?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// ===== Admin Types =====
export interface AdminNote {
  id: string;
  complaint_id: string;
  admin_id: string;
  admin?: Pick<User, 'name'>;
  content: string;
  is_internal: boolean;
  created_at: string;
}

export interface DashboardAnalytics {
  total_open: number;
  critical_count: number;
  high_count: number;
  avg_resolution_time_hours: number;
  satisfaction_score: number;
  complaints_by_category: Record<ComplaintCategory, number>;
  complaints_by_priority: Record<PriorityLevel, number>;
  trend: {
    this_week: number;
    last_week: number;
    change_percent: number;
  };
}

// ===== Pagination =====
export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
  };
}

// ===== Chat Types =====
export interface ChatMessage {
  id: string;
  role: 'user' | 'ai';
  content: string;
  timestamp: string;
  attachments?: string[];
  metadata?: {
    detected_category?: ComplaintCategory;
    detected_priority?: PriorityLevel;
    confidence?: number;
  };
}
