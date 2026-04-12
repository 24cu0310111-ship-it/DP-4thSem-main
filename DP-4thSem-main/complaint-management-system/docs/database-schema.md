# Database Schema Design

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE SCHEMA                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│      users       │       │    complaints    │       │ service_providers│
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │◄──────│ user_id (FK)     │       │ id (PK)          │
│ phone            │       │ id (PK)          │──────►│ platform         │
│ email            │       │ complaint_id     │       │ name             │
│ name             │       │ category         │       │ rating           │
│ password_hash    │       │ priority_level   │       │ service_types    │
│ role             │       │ status           │       │ service_areas    │
│ address (JSONB)  │       │ ai_analysis      │       │ deep_link        │
│ is_active        │       │ assigned_provider│       │ is_active        │
│ created_at       │       │ created_at       │       │ created_at       │
│ updated_at       │       │ updated_at       │       │ updated_at       │
└──────────────────┘       └──────────────────┘       └──────────────────┘
         │                         │
         │                         │
         ▼                         ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   audit_logs     │       │complaint_timeline│       │  admin_notes     │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │       │ complaint_id (FK)│       │ complaint_id (FK)│
│ action           │       │ event_type       │       │ admin_id (FK)    │
│ details (JSONB)  │       │ event_data (JSONB)│      │ content          │
│ ip_address       │       │ performed_by (FK)│       │ is_internal      │
│ created_at       │       │ created_at       │       │ created_at       │
└──────────────────┘       └──────────────────┘       └──────────────────┘
```

---

## Table Definitions

### users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| phone | VARCHAR(20) | UNIQUE, NOT NULL, INDEX | Primary contact |
| email | VARCHAR(255) | UNIQUE, INDEX | Optional email |
| name | VARCHAR(100) | NOT NULL | Full name |
| password_hash | VARCHAR(255) | NULLABLE | For password auth (NULL for OTP-only) |
| role | ENUM | NOT NULL, DEFAULT 'user' | user, admin, super_admin |
| address | JSONB | NOT NULL | Structured address |
| is_active | BOOLEAN | DEFAULT true | Soft delete |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Address JSONB Structure:**
```json
{
  "flat_no": "A-101",
  "building": "Sunrise Apartments",
  "street": "MG Road",
  "area": "Sector 15",
  "city": "Gurgaon",
  "state": "Haryana",
  "pincode": "122001",
  "coordinates": {
    "lat": 28.4595,
    "lng": 77.0266
  }
}
```

**Indexes:**
- `idx_users_phone` ON users(phone)
- `idx_users_email` ON users(email)
- `idx_users_role` ON users(role)
- `idx_users_address_area` ON users((address->>'area'))

---

### complaints

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Internal ID |
| complaint_id | VARCHAR(20) | UNIQUE, NOT NULL | User-facing ID (CM-YYYYMMDD-XXXX) |
| user_id | UUID | FK → users.id, NOT NULL | Complainant |
| category | ENUM | NOT NULL | electricity, water, sanitation, hvac, plumbing, maintenance, security, other |
| subcategory | VARCHAR(100) | NOT NULL | Specific sub-category |
| description | TEXT | NOT NULL | Full problem description |
| location | VARCHAR(255) | NOT NULL | Specific location within property |
| priority_level | ENUM | NOT NULL | critical, high, medium, low |
| priority_score | DECIMAL(5,2) | DEFAULT 0 | 0-100 score |
| priority_reasoning | TEXT | NULLABLE | AI explanation |
| status | ENUM | NOT NULL, DEFAULT 'open' | open, in_progress, assigned, resolved, closed, escalated |
| ai_analysis | JSONB | NULLABLE | Full NLU output from agents |
| media_urls | TEXT[] | ARRAY | S3 URLs of attached media |
| assigned_provider_id | UUID | FK → service_providers.id, NULLABLE | Assigned provider |
| assigned_admin_id | UUID | FK → users.id, NULLABLE | Handling admin |
| estimated_resolution_time | TIMESTAMPTZ | NULLABLE | ETA provided to user |
| actual_resolution_time | TIMESTAMPTZ | NULLABLE | Actual closure time |
| user_satisfaction | INTEGER | CHECK 1-5, NULLABLE | Rating after resolution |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**AI Analysis JSONB Structure:**
```json
{
  "category_confidence": 0.95,
  "subcategory_confidence": 0.87,
  "extracted_entities": {
    "location": "kitchen sink",
    "issue": "water leakage",
    "severity_words": ["flooding", "everywhere"]
  },
  "urgency_keywords": ["immediately", "urgent"],
  "affected_users": "single",
  "safety_risk": false,
  "detected_language": "hi",
  "sentiment_score": 0.78,
  "media_analysis": "Image shows active water leak from pipe joint"
}
```

**Indexes:**
- `idx_complaints_user_id` ON complaints(user_id)
- `idx_complaints_status` ON complaints(status)
- `idx_complaints_priority` ON complaints(priority_level)
- `idx_complaints_category` ON complaints(category)
- `idx_complaints_created` ON complaints(created_at DESC)
- `idx_complaints_assigned_provider` ON complaints(assigned_provider_id)

---

### service_providers

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | |
| platform | ENUM | NOT NULL | urban_company, taskrabbit, handy, local |
| platform_provider_id | VARCHAR(100) | UNIQUE | External platform ID |
| name | VARCHAR(255) | NOT NULL | Provider/business name |
| service_types | TEXT[] | ARRAY | Categories they serve |
| rating | DECIMAL(3,2) | CHECK 0-5 | Average rating |
| reviews_count | INTEGER | DEFAULT 0 | |
| price_range | ENUM | $, $$, $$$ | |
| service_areas | TEXT[] | ARRAY | Pin codes served |
| availability_status | ENUM | available, busy, unavailable | |
| avg_response_time | INTEGER | Minutes | |
| deep_link_template | VARCHAR(500) | URL template | |
| is_active | BOOLEAN | DEFAULT true | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Indexes:**
- `idx_providers_platform` ON service_providers(platform)
- `idx_providers_service_types` ON service_providers USING GIN(service_types)
- `idx_providers_service_areas` ON service_providers USING GIN(service_areas)
- `idx_providers_availability` ON service_providers(availability_status)

---

### complaint_timeline

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | |
| complaint_id | UUID | FK → complaints.id, NOT NULL | |
| event_type | ENUM | NOT NULL | created, prioritized, assigned, status_changed, provider_booked, resolved, escalated, commented |
| event_data | JSONB | NOT NULL | Event-specific data |
| performed_by | UUID | FK → users.id, NULLABLE | Who triggered this |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Event Data Examples:**
```json
// event_type: 'prioritized'
{
  "previous_priority": null,
  "new_priority": "high",
  "priority_score": 78.5,
  "reasoning": "Water leakage in kitchen affects daily living"
}

// event_type: 'assigned'
{
  "provider_id": "uuid",
  "provider_name": "ABC Plumbing",
  "platform": "urban_company",
  "admin_id": "uuid"
}

// event_type: 'status_changed'
{
  "previous_status": "open",
  "new_status": "in_progress",
  "admin_id": "uuid"
}
```

**Indexes:**
- `idx_timeline_complaint_id` ON complaint_timeline(complaint_id)
- `idx_timeline_created` ON complaint_timeline(created_at)
- `idx_timeline_event_type` ON complaint_timeline(event_type)

---

### admin_notes

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | |
| complaint_id | UUID | FK → complaints.id, NOT NULL | |
| admin_id | UUID | FK → users.id, NOT NULL | Note author |
| content | TEXT | NOT NULL | Note content |
| is_internal | BOOLEAN | DEFAULT true | Visible to admins only |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Indexes:**
- `idx_notes_complaint_id` ON admin_notes(complaint_id)
- `idx_notes_admin_id` ON admin_notes(admin_id)

---

### audit_logs

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | |
| user_id | UUID | FK → users.id, NULLABLE | Who performed action |
| action | VARCHAR(100) | NOT NULL | Action type |
| details | JSONB | NULLABLE | Action details |
| ip_address | INET | NULLABLE | Request IP |
| user_agent | VARCHAR(500) | NULLABLE | Browser/client |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Indexes:**
- `idx_audit_user_id` ON audit_logs(user_id)
- `idx_audit_action` ON audit_logs(action)
- `idx_audit_created` ON audit_logs(created_at)

---

## Migrations (Alembic)

Initial migration creates all tables with indexes. Subsequent migrations handle schema changes.

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

---

## Query Examples

### Get complaints by priority for admin dashboard
```sql
SELECT 
    c.complaint_id,
    c.category,
    c.priority_level,
    c.status,
    c.description,
    c.created_at,
    u.name as user_name,
    u.phone as user_phone
FROM complaints c
JOIN users u ON c.user_id = u.id
WHERE c.status IN ('open', 'in_progress')
ORDER BY 
    CASE c.priority_level 
        WHEN 'critical' THEN 1 
        WHEN 'high' THEN 2 
        WHEN 'medium' THEN 3 
        ELSE 4 
    END,
    c.created_at DESC
LIMIT 50;
```

### Get complaint timeline
```sql
SELECT 
    ct.event_type,
    ct.event_data,
    ct.created_at,
    u.name as performed_by_name
FROM complaint_timeline ct
LEFT JOIN users u ON ct.performed_by = u.id
WHERE ct.complaint_id = :complaint_id
ORDER BY ct.created_at ASC;
```

### Find available providers for category
```sql
SELECT 
    id,
    name,
    platform,
    rating,
    price_range,
    avg_response_time
FROM service_providers
WHERE :category = ANY(service_types)
  AND :pincode = ANY(service_areas)
  AND availability_status = 'available'
  AND is_active = true
ORDER BY rating DESC, avg_response_time ASC
LIMIT 10;
```

---

## Connection Pooling

Use connection pooling for optimal performance:

```python
# Using SQLAlchemy with asyncpg
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600
)
```
