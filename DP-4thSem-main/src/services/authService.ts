import type { LoginRequest, LoginResponse, User } from '../types';
import api from './api';

// ===== Mock Data (until backend is connected) =====
const MOCK_USERS: Record<string, { password: string; user: User }> = {
  '+919876543210': {
    password: 'user123',
    user: {
      id: '550e8400-e29b-41d4-a716-446655440000',
      phone: '+919876543210',
      email: 'sarah.chen@example.com',
      name: 'Sarah Chen',
      role: 'user',
      address: {
        flat_no: 'A-101',
        building: 'Skyview Towers',
        area: 'Sector 15',
        city: 'Gurgaon',
        pincode: '122001',
      },
      is_active: true,
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-15T10:30:00Z',
    },
  },
  admin: {
    password: 'admin123',
    user: {
      id: '550e8400-e29b-41d4-a716-446655440099',
      phone: '+919876543299',
      email: 'admin@scms.com',
      name: 'Marcus Thorne',
      role: 'admin',
      address: {
        flat_no: 'Office',
        building: 'SCMS HQ',
        area: 'Sector 1',
        city: 'Gurgaon',
        pincode: '122001',
      },
      is_active: true,
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    },
  },
};

const USE_MOCK = false; // Backend is live — using real API

function generateMockToken(): string {
  return 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.' +
    btoa(JSON.stringify({ exp: Date.now() + 86400000 })) +
    '.mock-signature';
}

export const authService = {
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    if (USE_MOCK) {
      const mockUser =
        credentials.phone === 'admin'
          ? MOCK_USERS['admin']
          : MOCK_USERS[credentials.phone];

      if (!mockUser || mockUser.password !== credentials.password) {
        throw new Error('Invalid credentials');
      }

      const token = generateMockToken();
      return {
        access_token: token,
        refresh_token: token + '-refresh',
        token_type: 'bearer',
        expires_in: 86400,
        user: {
          id: mockUser.user.id,
          name: mockUser.user.name,
          role: mockUser.user.role,
        },
      };
    }

    const { data } = await api.post<LoginResponse>('/auth/login', credentials);
    return data;
  },

  async getProfile(): Promise<User> {
    if (USE_MOCK) {
      const stored = localStorage.getItem('scms_user');
      if (stored) return JSON.parse(stored);
      throw new Error('Not authenticated');
    }

    const { data } = await api.get<User>('/user/profile');
    return data;
  },

  logout(): void {
    localStorage.removeItem('scms_token');
    localStorage.removeItem('scms_refresh_token');
    localStorage.removeItem('scms_user');
  },
};
