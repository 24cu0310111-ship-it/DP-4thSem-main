# API Specification

## Base URL
```
Production: https://api.scms.com/api/v1
Development: http://localhost:8000/api/v1
```

## Authentication
All authenticated endpoints require JWT token in header:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request:**
```json
{
  "phone": "+919876543210",
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePass123!",
  "address": {
    "flat_no": "A-101",
    "building": "Sunrise Apartments",
    "street": "MG Road",
    "area": "Sector 15",
    "city": "Gurgaon",
    "state": "Haryana",
    "pincode": "122001"
  }
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "phone": "+919876543210",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### POST /auth/login
Login with phone/email and password.

**Request:**
```json
{
  "phone": "+919876543210",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "role": "user"
  }
}
```

---

### POST /auth/otp/request
Request OTP for passwordless login.

**Request:**
```json
{
  "phone": "+919876543210"
}
```

**Response (200):**
```json
{
  "message": "OTP sent successfully",
  "expires_in": 300
}
```

---

### POST /auth/otp/verify
Verify OTP and get tokens.

**Request:**
```json
{
  "phone": "+919876543210",
  "otp": "123456"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

---

### POST /auth/refresh
Refresh access token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 86400
}
```

---

## User Endpoints

### GET /user/profile
Get current user profile.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "phone": "+919876543210",
  "email": "user@example.com",
  "address": {
    "flat_no": "A-101",
    "building": "Sunrise Apartments",
    "area": "Sector 15",
    "city": "Gurgaon",
    "pincode": "122001"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### PUT /user/profile
Update user profile.

**Request:**
```json
{
  "name": "John D Doe",
  "email": "newemail@example.com",
  "address": {
    "flat_no": "B-202",
    "building": "Sunrise Apartments",
    "area": "Sector 15",
    "city": "Gurgaon",
    "pincode": "122001"
  }
}
```

---

### GET /user/complaints
Get all complaints for current user.

**Query Parameters:**
- `status` (optional): Filter by status
- `priority` (optional): Filter by priority
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 20)

**Response (200):**
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "complaint_id": "CM-20240115-0001",
      "category": "plumbing",
      "subcategory": "pipe_leak",
      "description": "Water pipe leaking in kitchen",
      "priority_level": "high",
      "priority_score": 78.5,
      "status": "in_progress",
      "location": "kitchen sink",
      "created_at": "2024-01-15T11:00:00Z",
      "updated_at": "2024-01-15T12:30:00Z",
      "estimated_resolution_time": "2024-01-15T18:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 15,
    "total_pages": 1
  }
}
```

---

### POST /user/complaints
Register a new complaint.

**Request:**
```json
{
  "category": "plumbing",
  "subcategory": "pipe_leak",
  "description": "Water pipe leaking in kitchen, water spreading everywhere",
  "location": "kitchen sink area",
  "media_urls": ["https://s3.amazonaws.com/..."],
  "ai_analysis": {
    "category_confidence": 0.95,
    "extracted_entities": {...},
    "sentiment_score": 0.78,
    "detected_language": "en"
  }
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "complaint_id": "CM-20240115-0001",
  "category": "plumbing",
  "priority_level": "high",
  "priority_score": 78.5,
  "priority_reasoning": "Water leakage affects daily living and may cause property damage",
  "status": "open",
  "created_at": "2024-01-15T11:00:00Z",
  "message": "Complaint registered successfully. Expected response time: 4 hours"
}
```

---

### GET /user/complaints/:id
Get specific complaint details.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "complaint_id": "CM-20240115-0001",
  "category": "plumbing",
  "subcategory": "pipe_leak",
  "description": "Water pipe leaking in kitchen",
  "priority_level": "high",
  "priority_score": 78.5,
  "priority_reasoning": "Water leakage affects daily living...",
  "status": "in_progress",
  "location": "kitchen sink",
  "media_urls": ["https://s3.amazonaws.com/..."],
  "assigned_provider": {
    "id": "...",
    "name": "ABC Plumbing",
    "platform": "urban_company",
    "rating": 4.8
  },
  "estimated_resolution_time": "2024-01-15T18:00:00Z",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T12:30:00Z"
}
```

---

### GET /user/complaints/:id/timeline
Get complaint timeline.

**Response (200):**
```json
{
  "complaint_id": "CM-20240115-0001",
  "timeline": [
    {
      "event_type": "created",
      "event_data": {},
      "performed_by": null,
      "created_at": "2024-01-15T11:00:00Z"
    },
    {
      "event_type": "prioritized",
      "event_data": {
        "priority_level": "high",
        "priority_score": 78.5,
        "reasoning": "Water leakage affects daily living"
      },
      "performed_by": null,
      "created_at": "2024-01-15T11:00:05Z"
    },
    {
      "event_type": "assigned",
      "event_data": {
        "provider_name": "ABC Plumbing",
        "platform": "urban_company"
      },
      "performed_by": "Admin Name",
      "created_at": "2024-01-15T12:30:00Z"
    }
  ]
}
```

---

### POST /user/complaints/:id/escalate
Escalate a complaint.

**Request:**
```json
{
  "reason": "No response for 24 hours, issue getting worse"
}
```

**Response (200):**
```json
{
  "message": "Complaint escalated successfully",
  "new_priority": "critical",
  "escalation_id": "ESC-20240116-0001"
}
```

---

## Admin Endpoints

### GET /admin/complaints
Get all complaints with filters.

**Query Parameters:**
- `priority`: critical,high,medium,low (comma-separated)
- `status`: open,in_progress,assigned,resolved (comma-separated)
- `category`: electricity,water,etc. (comma-separated)
- `area`: filter by area
- `from_date`: YYYY-MM-DD
- `to_date`: YYYY-MM-DD
- `page`: number
- `limit`: number
- `sort`: priority,created_at (default: created_at DESC)

**Response (200):**
```json
{
  "data": [
    {
      "id": "...",
      "complaint_id": "CM-20240115-0001",
      "user": {
        "name": "John Doe",
        "phone": "+919876543210",
        "area": "Sector 15"
      },
      "category": "plumbing",
      "priority_level": "high",
      "status": "open",
      "description": "Water pipe leaking...",
      "created_at": "2024-01-15T11:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 234,
    "total_pages": 5
  }
}
```

---

### GET /admin/complaints/:id
Get full complaint details for admin.

**Response (200):**
```json
{
  "id": "...",
  "complaint_id": "CM-20240115-0001",
  "user": {
    "name": "John Doe",
    "phone": "+919876543210",
    "email": "user@example.com",
    "address": {...}
  },
  "category": "plumbing",
  "description": "Water pipe leaking...",
  "priority_level": "high",
  "priority_reasoning": "...",
  "status": "open",
  "ai_analysis": {...},
  "media_urls": [...],
  "timeline": [...],
  "notes": [...]
}
```

---

### PUT /admin/complaints/:id/status
Update complaint status.

**Request:**
```json
{
  "status": "in_progress",
  "note": "Assigned to plumber, arriving in 2 hours"
}
```

**Response (200):**
```json
{
  "message": "Status updated successfully",
  "complaint": {
    "id": "...",
    "status": "in_progress",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

---

### PUT /admin/complaints/:id/assign
Assign provider to complaint.

**Request:**
```json
{
  "provider_id": "550e8400-e29b-41d4-a716-446655440002",
  "estimated_time": "2024-01-15T18:00:00Z",
  "notes": "Customer prefers morning visit"
}
```

**Response (200):**
```json
{
  "message": "Provider assigned successfully",
  "provider": {
    "name": "ABC Plumbing",
    "platform": "urban_company",
    "phone": "+919876543211"
  },
  "booking_url": "https://urbancompany.com/booking/..."
}
```

---

### GET /admin/providers
Get all service providers.

**Query Parameters:**
- `platform`: urban_company,taskrabbit,handy,local
- `category`: filter by service type
- `area`: filter by service area
- `availability`: available,busy,unavailable
- `min_rating`: minimum rating filter

**Response (200):**
```json
{
  "data": [
    {
      "id": "...",
      "name": "ABC Plumbing",
      "platform": "urban_company",
      "service_types": ["plumbing", "water"],
      "rating": 4.8,
      "reviews_count": 234,
      "price_range": "$$",
      "availability_status": "available",
      "avg_response_time": 45,
      "service_areas": ["122001", "122002"]
    }
  ]
}
```

---

### POST /admin/complaints/:id/notes
Add internal note.

**Request:**
```json
{
  "content": "Customer called twice, very frustrated",
  "is_internal": true
}
```

**Response (201):**
```json
{
  "id": "...",
  "content": "Customer called twice...",
  "admin": {
    "name": "Admin Name"
  },
  "is_internal": true,
  "created_at": "2024-01-15T14:00:00Z"
}
```

---

### GET /admin/analytics/overview
Get dashboard analytics.

**Response (200):**
```json
{
  "total_open": 45,
  "critical_count": 3,
  "high_count": 12,
  "avg_resolution_time_hours": 18.5,
  "satisfaction_score": 4.2,
  "complaints_by_category": {
    "electricity": 15,
    "water": 12,
    "plumbing": 10,
    "other": 8
  },
  "complaints_by_priority": {
    "critical": 3,
    "high": 12,
    "medium": 20,
    "low": 10
  },
  "trend": {
    "this_week": 45,
    "last_week": 38,
    "change_percent": 18.4
  }
}
```

---

## WebSocket Events

### Connection
```
WS /ws/complaints/:id?token=<access_token>
```

### Server → Client Events

**complaint:updated**
```json
{
  "type": "complaint:updated",
  "data": {
    "complaint_id": "CM-20240115-0001",
    "status": "in_progress",
    "updated_at": "2024-01-15T12:00:00Z"
  }
}
```

**complaint:assigned**
```json
{
  "type": "complaint:assigned",
  "data": {
    "complaint_id": "CM-20240115-0001",
    "provider_name": "ABC Plumbing",
    "estimated_time": "2024-01-15T18:00:00Z"
  }
}
```

**notification:new**
```json
{
  "type": "notification:new",
  "data": {
    "id": "...",
    "title": "Complaint Updated",
    "message": "Your complaint status has changed",
    "type": "status_change"
  }
}
```

### Client → Server Events

**subscribe**
```json
{
  "type": "subscribe",
  "data": {
    "complaint_ids": ["CM-20240115-0001", "..."]
  }
}
```

**acknowledge**
```json
{
  "type": "acknowledge",
  "data": {
    "notification_id": "..."
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "validation_error",
  "message": "Invalid input data",
  "details": [
    {
      "field": "phone",
      "message": "Invalid phone number format"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "error": "unauthorized",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "forbidden",
  "message": "Admin access required"
}
```

### 404 Not Found
```json
{
  "error": "not_found",
  "message": "Complaint not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "internal_error",
  "message": "An unexpected error occurred",
  "reference_id": "ERR-20240115-ABC123"
}
```

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Auth endpoints | 10 requests/minute |
| User complaint CRUD | 60 requests/minute |
| Admin endpoints | 100 requests/minute |
| File upload | 10 requests/minute |
| WebSocket | 100 messages/second |

Rate limit headers included:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705320000
```
