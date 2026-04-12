# SCMS Project Handoff & Status Document

> **Note:** The webpaths detailed in this document are incomplete. The correct webpath should be like @[DP-4thSem-main/complaint-management-system/stitch_webpath.txt].

Hello Teammate Agent! You are taking over the **Smart Complaint Management System (SCMS)** project. This document serves as your complete context to pick up right where the previous agent left off without skipping a beat.

## 📌 Project Overview
SCMS is a full-stack application.
- **Frontend:** React + Vite (running on port 5173).
- **Backend:** FastAPI + MongoDB (running on port 8000).
- **AI Integration:** Sarvam AI via LangChain for NLU, prioritization, and provider assignment.

## ✅ Past Work Completed

1. **Backend Architecture & Database Setup:**
   - Established FastAPI backend with an async MongoDB (Motor) setup. 
   - Local MongoDB is currently running using the downloaded macOS aarch64 binary (`backend/mongodb_data`).
   - Defined Pydantic data models & schemas (`user`, `complaint`, `provider`, `timeline`, `auth`).

2. **API Endpoints Implemented:**
   - **Auth:** JWT-based login, register, refresh (`app/api/routes/auth.py`). 
   - **User:** Profile CRUD, User Complaints History, Complaint creation, Escalation (`app/api/routes/users.py`).
   - **Admin:** Aggregated analytics, status updates, assign providers, add admin notes (`app/api/routes/admin.py`).
   - **Providers:** Filtered listing of service providers (`app/api/routes/providers.py`).

3. **Frontend-Backend Integration:**
   - Seeded MongoDB exactly matching the frontend's mock data using `backend/seed_data.py`.
   - Replaced all mock flags in the frontend (`src/services/` -> `USE_MOCK = false`).
   - Conducted a successful end-to-end integration test (User and Admin login flows work flawlessly and pull correct real-time data from MongoDB).

4. **Initial AI Setup:**
   - Verified the **Sarvam AI API** key and connected using the `sarvam-m` model via an OpenAI compatible interface.
   - Built the Sarvam wrapper `app/agents/sarvam_llm.py`.
   - Built the deterministic prioritization engine `app/agents/prioritization.py`.
   - Built the AI NLU agent `app/agents/input_understanding.py`.
   - Built the AI Provider Matching agent `app/agents/assignment.py`.

## ✅ Phase 2 Work Completed (AI Pipeline & Chat)

We successfully finalized the **LangChain AI Agent pipeline**.

1. **Pipeline Orchestration (`app/agents/pipeline.py`):** Created the orchestration logic tying together Input Understanding, Prioritization, and Assignment into one seamless workflow.
2. **AI Chat API & Frontend Connection:** Established `/user/chat` endpoints for live AI complaint assistance in `app/api/routes/chat.py` and updated the frontend (`src/pages/AIChatIntake.tsx`) to pull actual response data and metadata, retiring the mock functions.
3. **Hooked AI into Complaints Router:** `app/api/routes/users.py` now invokes the full AI pipeline when a user submits a new complaint, automatically extracting category, severity, intent, and auto-assigning providers.

## 🚀 Future Work & Next Steps Guidance

To comfortably continue the work, please execute the following:

1. **Verify AI Flow Contextually:** Run an end-to-end test where a user interacts with the AI Chat in the frontend to file a complaint, verifying that the actual Sarvam AI processing returns appropriate insights accurately down the pipeline.
2. **Add WebSockets (Optional):** Implement real-time status updates/notifications pushed back to the frontend.
3. **Containerize Stack (Optional):** Package into Docker to make local scaling robust and detach from host environment subtleties.

## 🔧 Useful Details for You
- **Backend Directory:** `/Users/tejeshreddydevireddy/DP-4thSem/backend/`
- **Virtual Environment:** `venv`
- **Starting Backend:** `source venv/bin/activate && uvicorn app.main:app --reload --port 8000 --host 0.0.0.0`
- **Starting Frontend:** `cd frontend && npm run dev`
- **Demo Users:** 
    - User (Sarah Chen): `+919876543210` / `user123`
    - Admin (Marcus Thorne): `admin` / `admin123`

You should start by taking a quick look at `app/api/routes/users.py` and `app/agents/` to familiarize yourself with the structure! Good luck!
