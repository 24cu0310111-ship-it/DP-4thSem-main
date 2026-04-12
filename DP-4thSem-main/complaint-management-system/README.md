# Smart Complaint Management System (SCMS)

> **Note:** The webpaths detailed in this document are incomplete. The correct webpath should be like @[DP-4thSem-main/complaint-management-system/stitch_webpath.txt].

## Overview
An AI-driven complaint management platform for urban residential and commercial areas that leverages LangChain and Sarvam AI for intelligent problem classification, prioritization, and resolution coordination.

## Problem Statement
- Delays in resolving utility and maintenance complaints
- Lack of intelligent prioritization
- Poor coordination between stakeholders
- No real-time tracking

## Solution
A unified platform with:
1. **AI Input Understanding Agent** - NLU + Multimedia processing
2. **Intelligent Prioritization** - Severity scoring based on multiple factors
3. **Admin Dashboard** - Aggregated service provider comparison & booking
4. **User Portal** - Easy complaint registration with tracking

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  User Mobile/Web App    │    Admin Web Dashboard                 │
│  - Auth                 │    - Auth                              │
│  - Register Complaint   │    - Complaint Panel                   │
│  - Track History        │    - Service Provider Marketplace      │
│  - Real-time Updates    │    - Booking & Assignment              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  REST APIs │ WebSocket │ File Upload │ Notification Service     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI AGENT LAYER (LangChain)                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Input Understanding Agent                       │   │
│  │  - Text NLU (Sarvam AI)                                   │   │
│  │  - Image Analysis (Multimedia)                            │   │
│  │  - Voice/ Audio Processing                                │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Prioritization Agent                            │   │
│  │  - Severity Scoring                                       │   │
│  │  - Category Classification                                │   │
│  │  - Urgency Detection                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Assignment Agent                                │   │
│  │  - Service Provider Matching                              │   │
│  │  - Location-based Filtering                               │   │
│  │  - Price Comparison                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                   │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL (Users, Complaints)  │  Redis (Cache, Sessions)    │
│  MongoDB (Chat History, Logs)    │  S3 (Media Storage)         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 EXTERNAL INTEGRATIONS                            │
├─────────────────────────────────────────────────────────────────┤
│  Urban Company API │ TaskRabbit API │ Handy API │ SMS/Email    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14 + TypeScript + TailwindCSS |
| Mobile | React Native / Flutter |
| Backend | Python FastAPI |
| AI Framework | LangChain + Sarvam AI |
| Database | PostgreSQL + MongoDB |
| Cache | Redis |
| Storage | AWS S3 / Cloudflare R2 |
| Real-time | WebSocket / Socket.io |
| Auth | JWT + OAuth2 |

---

## Key Features

### User Features
1. **Authentication** - Phone/Email + OTP
2. **Complaint Registration** - Chatbot with text, image, voice support
3. **Priority Display** - AI-assigned urgency badges
4. **History Tracking** - Timeline view with status updates
5. **Notifications** - Real-time updates via push/SMS

### Admin Features
1. **Dashboard** - Overview with priority-sorted complaints
2. **Service Provider Marketplace** - Filter by:
   - Location/Service Area
   - Price Range
   - Ratings & Reviews
   - Availability
   - Service Type
3. **One-Click Booking** - Deep link to provider app/website
4. **Analytics** - Resolution time, satisfaction scores

### AI Agent Features
1. **Multi-modal Input Processing**
   - Text understanding (Sarvam AI for Indian languages)
   - Image analysis (damage assessment, issue identification)
   - Voice transcription and sentiment

2. **Prioritization Matrix**
   ```
   Priority = f(Impact, Urgency, Affected Users, Safety Risk)
   
   Factors:
   - Category Weight (Electricity > Maintenance)
   - Severity Level (Critical/High/Medium/Low)
   - Time Sensitivity (Immediate/Within 24h/Within Week)
   - Safety Impact (Yes/No)
   - Affected Population (Single/Multiple/Building)
   ```

3. **Category Classification**
   - Electricity
   - Water Supply
   - Sanitation
   - HVAC
   - Plumbing
   - General Maintenance
   - Security
   - Other

---

## Project Structure

```
scms/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── agents/
│   │   │   ├── input_understanding.py
│   │   │   ├── prioritization.py
│   │   │   └── assignment.py
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   └── package.json
├── mobile/
│   └── src/
├── docs/
│   ├── api-spec.md
│   ├── agent-design.md
│   └── database-schema.md
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Sarvam AI API Key
- LangChain setup

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/scms.git
cd scms

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
npm run dev
```

---

## License
MIT
