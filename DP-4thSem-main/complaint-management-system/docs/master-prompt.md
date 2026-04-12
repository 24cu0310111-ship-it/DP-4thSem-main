# Master Prompt for AI Code Generation (Antigravity/Cursor/Claude)

## Complete System Build Prompt

```
You are building a complete Smart Complaint Management System (SCMS) - an AI-powered platform for urban residential and commercial complaint resolution using LangChain and Sarvam AI.

## Project Overview

This system solves delays in urban service complaints (electricity, water, sanitation, maintenance) by:
1. Using AI to understand complaints in natural language + multimedia
2. Automatically prioritizing based on severity (like a human administrator)
3. Connecting admins to service providers (Urban Company, TaskRabbit, Handy)
4. Providing real-time tracking for users

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI (web framework)
- LangChain (AI orchestration)
- Sarvam AI (NLU for Indian languages)
- PostgreSQL (primary database)
- MongoDB (chat history, logs)
- Redis (cache, sessions, task queue)
- Celery (async tasks)
- Socket.IO (real-time updates)

**Frontend:**
- Next.js 14 App Router
- TypeScript
- TailwindCSS
- shadcn/ui components
- Zustand (state)
- Socket.IO client

**Mobile:**
- React Native (optional phase 2)

**Infrastructure:**
- Docker + Docker Compose
- Nginx (reverse proxy)
- AWS S3 (media storage)

---

## Phase 1: Backend Implementation

### Step 1: Project Setup

Create the following structure:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Settings, env variables
│   ├── database.py          # DB connections
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── complaint.py     # Complaint model
│   │   ├── provider.py      # Service provider model
│   │   └── audit.py         # Audit log model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic schemas
│   │   ├── complaint.py
│   │   ├── provider.py
│   │   └── ai_responses.py  # AI agent output schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (auth, DB)
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py      # Auth endpoints
│   │   │   ├── users.py     # User endpoints
│   │   │   ├── complaints.py # Complaint CRUD
│   │   │   ├── admin.py     # Admin endpoints
│   │   │   └── providers.py # Provider endpoints
│   │   └── websocket.py     # WebSocket handler
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py          # Base agent class
│   │   ├── input_understanding.py  # NLU agent
│   │   ├── prioritization.py       # Priority agent
│   │   ├── assignment.py           # Provider matching
│   │   └── pipeline.py      # Full agent pipeline
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py          # Auth logic
│   │   ├── complaints.py    # Complaint business logic
│   │   ├── providers.py     # Provider integration
│   │   ├── notifications.py # SMS, Email, Push
│   │   └── media.py         # File upload handling
│   └── utils/
│       ├── __init__.py
│       ├── security.py      # JWT, password hashing
│       ├── sarvam_client.py # Sarvam AI wrapper
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_agents.py
│   ├── test_api.py
│   └── test_services.py
├── alembic/                 # Database migrations
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── .env.example
```

### Step 2: Core Models

Implement these SQLAlchemy models:

**User Model:**
```python
- id: UUID (primary key)
- phone: String (unique, indexed)
- email: String (unique)
- name: String
- password_hash: String (nullable for OTP users)
- role: Enum (user, admin, super_admin)
- address: JSONB (flat_no, building, street, area, city, pincode, coordinates)
- is_active: Boolean
- created_at: DateTime
- updated_at: DateTime
```

**Complaint Model:**
```python
- id: UUID (primary key)
- complaint_id: String (unique, format: CM-YYYYMMDD-XXXX)
- user_id: ForeignKey(User)
- category: Enum (electricity, water, sanitation, hvac, plumbing, maintenance, security, other)
- subcategory: String
- description: Text
- location: String (specific location within property)
- priority_level: Enum (critical, high, medium, low)
- priority_score: Float (0-100)
- priority_reasoning: Text (AI explanation)
- status: Enum (open, in_progress, assigned, resolved, closed, escalated)
- ai_analysis: JSONB (full NLU output)
- media_urls: Array[String]
- assigned_provider_id: ForeignKey(ServiceProvider, nullable)
- assigned_admin_id: ForeignKey(User, nullable)
- estimated_resolution_time: DateTime (nullable)
- actual_resolution_time: DateTime (nullable)
- user_satisfaction: Integer (1-5, nullable)
- created_at: DateTime
- updated_at: DateTime
```

**ServiceProvider Model:**
```python
- id: UUID (primary key)
- platform: Enum (urban_company, taskrabbit, handy, local)
- platform_provider_id: String (external ID)
- name: String
- service_types: Array[String]
- rating: Float
- reviews_count: Integer
- price_range: Enum ($, $$, $$$)
- service_areas: Array[String] (pin codes served)
- availability_status: Enum (available, busy, unavailable)
- avg_response_time: Integer (minutes)
- deep_link_template: String (URL template for booking)
- is_active: Boolean
```

**ComplaintTimeline Model:**
```python
- id: UUID (primary key)
- complaint_id: ForeignKey(Complaint)
- event_type: Enum (created, prioritized, assigned, status_changed, provider_booked, resolved, escalated, commented)
- event_data: JSONB
- performed_by: ForeignKey(User, nullable)
- created_at: DateTime
```

### Step 3: AI Agents Implementation

Use LangChain to implement:

**Input Understanding Agent:**
- Integrate Sarvam AI for Indian language NLU
- Process text, extract entities (location, category, issue)
- Handle image attachments (describe the problem)
- Handle voice notes (transcribe + analyze)
- Output: Structured ComplaintInput schema

**Prioritization Agent:**
- Take structured complaint input
- Apply priority matrix (category weight, safety, urgency, affected users, sentiment)
- Generate human-readable reasoning
- Output: Priority level + score + explanation

**Assignment Agent:**
- Query service provider database
- Filter by category, location, availability
- Rank by rating, price, distance
- Output: Top 5 provider recommendations

### Step 4: API Endpoints

Implement these REST endpoints:

**Authentication:**
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- POST /api/v1/auth/otp/request
- POST /api/v1/auth/otp/verify
- POST /api/v1/auth/refresh
- POST /api/v1/auth/logout

**User:**
- GET /api/v1/user/profile
- PUT /api/v1/user/profile
- GET /api/v1/user/complaints
- POST /api/v1/user/complaints
- GET /api/v1/user/complaints/{id}
- GET /api/v1/user/complaints/{id}/timeline
- POST /api/v1/user/complaints/{id}/escalate

**Admin:**
- GET /api/v1/admin/complaints (with filters)
- GET /api/v1/admin/complaints/{id}
- PUT /api/v1/admin/complaints/{id}/status
- PUT /api/v1/admin/complaints/{id}/assign
- GET /api/v1/admin/providers
- GET /api/v1/admin/analytics/overview
- POST /api/v1/admin/complaints/{id}/notes

**WebSocket:**
- WS /ws/complaints/{id} (real-time updates)

### Step 5: Real-time Updates

Implement WebSocket handler for:
- New complaint notifications to admin
- Status change notifications to user
- Chat updates
- Provider assignment alerts

---

## Phase 2: Frontend Implementation

### File Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── (public)/
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── (auth)/
│   │   │   ├── user/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── register/page.tsx
│   │   │   └── admin/
│   │   │       └── login/page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── user/
│   │   │   │   ├── dashboard/page.tsx
│   │   │   │   ├── complaints/
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   ├── new/page.tsx
│   │   │   │   │   └── [id]/page.tsx
│   │   │   └── admin/
│   │   │       ├── dashboard/page.tsx
│   │   │       ├── complaints/page.tsx
│   │   │       ├── complaints/[id]/page.tsx
│   │   │       ├── providers/page.tsx
│   │   │       └── analytics/page.tsx
│   │   └── api/ (API routes if needed)
│   ├── components/
│   │   ├── ui/ (shadcn components)
│   │   ├── shared/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── PriorityBadge.tsx
│   │   │   ├── StatusBadge.tsx
│   │   │   └── ...
│   │   ├── user/
│   │   │   ├── ComplaintCard.tsx
│   │   │   ├── ChatbotInterface.tsx
│   │   │   ├── Timeline.tsx
│   │   │   └── ...
│   │   └── admin/
│   │       ├── ComplaintTable.tsx
│   │       ├── ProviderCard.tsx
│   │       ├── ProviderMarketplace.tsx
│   │       └── ...
│   ├── lib/
│   │   ├── api.ts (axios instance)
│   │   ├── websocket.ts
│   │   ├── utils.ts
│   │   └── constants.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useComplaints.ts
│   │   ├── useWebSocket.ts
│   │   └── ...
│   ├── store/
│   │   ├── index.ts (zustand)
│   │   ├── authStore.ts
│   │   ├── complaintStore.ts
│   │   └── ...
│   └── types/
│       └── index.ts
├── public/
├── tailwind.config.ts
├── next.config.js
├── package.json
└── tsconfig.json
```

### Key Components to Implement

**User Chatbot Interface:**
- Full-screen chat for complaint registration
- Message bubbles (user right/blue, AI left/gray)
- Attachment buttons (photo, voice, document)
- Language selector
- Typing indicators
- State machine: idle → collecting → confirming → submitted

**Admin Complaint Panel:**
- Data table with sorting, filtering, pagination
- Priority badges with colors
- Quick actions (assign, status change)
- Bulk operations

**Provider Marketplace:**
- Grid of provider cards
- Filter sidebar (collapsible on mobile)
- Platform badges (UC, TR, Handy icons)
- "Book Now" → deep link or modal

---

## Phase 3: Integration & Testing

### Docker Compose Setup

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
      - SARVAM_API_KEY=${SARVAM_API_KEY}
    depends_on: [postgres, redis]

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [backend]

  postgres:
    image: postgres:15
    volumes: [postgres_data:/var/lib/postgresql/data]

  redis:
    image: redis:7

  celery-worker:
    build: ./backend
    command: celery -A app.celery worker -l info
    depends_on: [redis, postgres]

volumes:
  postgres_data:
```

### Testing Strategy

1. **Unit Tests:** Pytest for backend, Jest for frontend
2. **Integration Tests:** API endpoint testing
3. **Agent Tests:** Verify AI outputs with known inputs
4. **E2E Tests:** Playwright for critical user flows

---

## Implementation Order

1. ✅ Backend models and database setup
2. ✅ Authentication APIs
3. ✅ Complaint CRUD APIs
4. ✅ AI agent pipeline
5. ✅ WebSocket real-time
6. ✅ Frontend user dashboard
7. ✅ Frontend admin dashboard
8. ✅ Provider marketplace
9. ✅ Integration testing
10. ✅ Deployment configuration

---

## Important Notes

1. **Sarvam AI Integration:** Use official SDK or REST API. Support all Indian languages.

2. **Priority Logic:** Must be explainable. Admin should understand WHY a complaint got its priority.

3. **Security:**
   - JWT with refresh tokens
   - Password hashing (argon2)
   - Input validation on all endpoints
   - Rate limiting
   - CORS configuration

4. **Media Handling:**
   - Upload to S3 with presigned URLs
   - Virus scanning
   - Image compression
   - EXIF data stripping

5. **Accessibility:**
   - WCAG 2.1 AA
   - Keyboard navigation
   - Screen reader support

6. **Performance:**
   - Database indexing on frequently queried fields
   - Redis caching for provider lists
   - Pagination on all list endpoints
   - Lazy loading on frontend

---

Generate complete, production-ready code following these specifications. Use TypeScript strictly. Include error handling, loading states, and proper logging throughout.
```

---

## Environment Variables Template

```bash
# .env.example

# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/scms
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://localhost:27017/scms

# Security
SECRET_KEY=your-secret-key-here
JWT_EXPIRY_HOURS=24
REFRESH_TOKEN_EXPIRY_DAYS=30

# Sarvam AI
SARVAM_API_KEY=your-sarvam-api-key

# Storage (S3)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_BUCKET_NAME=scms-media
AWS_REGION=ap-south-1

# Notifications
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
SENDGRID_API_KEY=
FCM_SERVER_KEY=

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```
