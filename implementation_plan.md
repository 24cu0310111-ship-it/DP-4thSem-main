# SCMS Backend — AI Pipeline & Chat API Completion

## Background

The SCMS (Smart Complaint Management System) backend is built with **FastAPI + MongoDB (Motor) + Pydantic** and has partial AI integration via **Sarvam AI + LangChain**. The frontend is complete and should not be touched unless strictly necessary.

### What's Already Done
- FastAPI app with CORS, lifespan, JWT auth, and 4 route modules (auth, users, admin, providers)
- MongoDB async connection (Motor), collection accessors, indexes, seed data
- Pydantic models/schemas for User, Complaint, Provider, Timeline
- Three individual AI agents: `input_understanding.py`, `prioritization.py`, `assignment.py`
- Sarvam AI LLM wrapper (`sarvam_llm.py`) with both LangChain and direct `httpx` modes
- Frontend `AIChatIntake.tsx` currently **simulates** AI responses client-side — needs a real backend chat endpoint

### What's Missing (from CONTINUE.md)
1. **`app/agents/pipeline.py`** — Orchestrator tying NLU → Prioritization → Assignment into one flow
2. **`users.py` POST `/complaints`** — Currently only uses deterministic `calculate_priority_score`; needs full AI pipeline
3. **`/user/chat` endpoint** — Backend chat API so the frontend `AIChatIntake.tsx` can call real AI instead of simulating
4. **`.env` file** — Not yet created (only `.env.example` exists)

---

## User Review Required

> [!IMPORTANT]
> The frontend `AIChatIntake.tsx` currently uses a `simulateAIResponse()` function with hardcoded responses. To make the AI chat **actually work**, the frontend will need a **minimal** update to call the new `/user/chat` endpoint instead. This is the **only** frontend change needed.

> [!IMPORTANT]
> You will need a **Sarvam AI API key** in the `.env` file for AI features to work. Without it, the system gracefully falls back to deterministic keyword-based analysis (which still works perfectly).

---

## Proposed Changes

### Component 1: AI Pipeline Orchestrator

#### [NEW] [pipeline.py](file:///d:/Download/DP-4thSem-main/DP-4thSem-main/backend/app/agents/pipeline.py)

Creates the missing orchestration layer that:
1. Takes raw complaint text + optional metadata (location, user info)
2. Calls `input_understanding.analyze_complaint()` → extracts category, urgency, safety, sentiment
3. Calls `prioritization.calculate_priority_score()` → produces priority level + score
4. Calls `assignment.find_best_provider()` → suggests best provider
5. Returns a unified `PipelineResult` dict with all enriched data

```python
async def run_complaint_pipeline(description, location, user_info) -> dict
```

---

### Component 2: AI Chat Endpoint

#### [NEW] [chat.py](file:///d:/Download/DP-4thSem-main/DP-4thSem-main/backend/app/api/routes/chat.py)

A new route file for the AI chat assistant with endpoints:

- **`POST /user/chat`** — Send a message to the AI assistant, receive a response with NLU metadata (category, priority, confidence). Manages conversation context via `chat_history` MongoDB collection (already has an accessor in `database.py`).
- **`POST /user/chat/file-complaint`** — When the user confirms, creates a real complaint using the full AI pipeline.
- **`GET /user/chat/history`** — Retrieve past chat sessions.

The chat endpoint will:
1. Store user message in `chat_history` collection
2. Send message to Sarvam AI via `sarvam_chat()` with a complaint-assistant system prompt
3. Run NLU analysis on the message to extract category/priority metadata
4. Return the AI response + metadata to the frontend
5. When user confirms filing → trigger the full `pipeline.py` orchestrator

---

### Component 3: Integrate AI Pipeline into Complaint Creation

#### [MODIFY] [users.py](file:///d:/Download/DP-4thSem-main/DP-4thSem-main/backend/app/api/routes/users.py)

Update `POST /complaints` to invoke the full AI pipeline:

```diff
- from app.agents.prioritization import calculate_priority_score
- priority_result = calculate_priority_score(category=..., safety_risk=False, ...)
+ from app.agents.pipeline import run_complaint_pipeline
+ pipeline_result = await run_complaint_pipeline(description, location, user_info)
```

The complaint document will now be enriched with:
- AI-detected `category` (confirming or overriding user input)
- `subcategory` from NLU
- `ai_analysis` field with full NLU results
- Accurate `priority_level` and `priority_score` from weighted formula using AI inputs
- Optional `assigned_provider_id` from auto-assignment agent
- Timeline events for each pipeline step (NLU, prioritization, assignment)

---

### Component 4: Chat Schema

#### [NEW] [chat.py](file:///d:/Download/DP-4thSem-main/DP-4thSem-main/backend/app/schemas/chat.py)

Pydantic schemas for chat request/response:
- `ChatMessageRequest` — user message text + optional session_id
- `ChatMessageResponse` — AI response + metadata (category, priority, confidence)
- `FileComplaintFromChatRequest` — confirm and file complaint from chat context

---

### Component 5: Register Chat Router

#### [MODIFY] [main.py](file:///d:/Download/DP-4thSem-main/DP-4thSem-main/backend/app/main.py)

Add the chat router:
```python
from app.api.routes import auth, users, admin, providers, chat
app.include_router(chat.router, prefix=f"{settings.API_PREFIX}/user", tags=["Chat"])
```

---

### Component 6: Environment & Dependencies

#### [NEW] [.env](file:///d:/Download/DP-4thSem-main/DP-4thSem-main/backend/.env)

Copy from `.env.example` with sensible defaults. User must fill `SARVAM_API_KEY`.

#### [MODIFY] [requirements.txt](file:///d:/Download/DP-4thSem-main/DP-4thSem-main/backend/requirements.txt)

Add `langchain-openai` for the `ChatOpenAI` import used in `sarvam_llm.py` (currently imports from deprecated `langchain.chat_models`).

---

### Component 7: Frontend Minimal Update (Only if necessary)

#### [MODIFY] [AIChatIntake.tsx](file:///d:/Download/DP-4thSem-main/DP-4thSem-main/src/pages/AIChatIntake.tsx)

Replace `simulateAIResponse()` with real API calls to `POST /user/chat`. This is the **only** frontend change — the UI/UX stays identical but now uses live AI responses.

---

## Open Questions

> [!IMPORTANT]
> **Sarvam API Key**: Do you have a Sarvam AI API key to put in the `.env` file? Without it, the system will work fine using deterministic fallbacks, but the chat and AI analysis won't use the LLM.

> [!IMPORTANT]
> **MongoDB**: The CONTINUE.md mentions MongoDB was running from a macOS binary. Since you're on **Windows**, do you have MongoDB installed and running locally? I'll need it running on `localhost:27017` for the backend.

---

## Verification Plan

### Automated Tests
1. **Start the backend**: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000`
2. **Seed the database**: `python seed_data.py`
3. **cURL test — login**: `POST /api/v1/auth/login` with user credentials
4. **cURL test — create complaint**: `POST /api/v1/user/complaints` and verify AI pipeline is invoked
5. **cURL test — AI chat**: `POST /api/v1/user/chat` with a message and verify AI response + metadata
6. **cURL test — file from chat**: `POST /api/v1/user/chat/file-complaint` and verify complaint is created

### Manual Verification
1. Start backend + frontend, login as Sarah Chen
2. Go to "AI Chat" — send a complaint description → verify real AI response appears
3. Confirm filing → verify complaint appears in history with AI-enriched data
4. Login as admin → verify the complaint shows AI analysis and proper priority

### Files Created/Modified Summary
| Action | File |
|--------|------|
| **NEW** | `backend/app/agents/pipeline.py` |
| **NEW** | `backend/app/api/routes/chat.py` |
| **NEW** | `backend/app/schemas/chat.py` |
| **NEW** | `backend/.env` |
| **MODIFY** | `backend/app/api/routes/users.py` |
| **MODIFY** | `backend/app/main.py` |
| **MODIFY** | `backend/requirements.txt` |
| **MODIFY** | `src/pages/AIChatIntake.tsx` (minimal — API calls only) |
