# Code Review Graph - Smart Complaint Management System

> **Note:** The webpaths detailed in this document are incomplete. The correct webpath should be like @[DP-4thSem-main/complaint-management-system/stitch_webpath.txt].

## 1. High-Level Architecture

```mermaid
graph TB
    subgraph Client["Frontend (React/TypeScript/Vite)"]
        UI["./src/pages/*"]
        COMP["./src/components/*"]
        HOOKS["./src/hooks/*"]
        SERVICES["./src/services/*"]
    end

    subgraph Server["Backend (Python/FastAPI)"]
        API["./app/api/routes/*"]
        MODELS["./app/models/*"]
        SCHEMAS["./app/schemas/*"]
        AGENTS["./app/agents/*"]
        SERVICES_B["./app/services/*"]
        UTILS["./app/utils/*"]
    end

    DB[(MongoDB)]

    UI --> HOOKS
    UI --> COMP
    HOOKS --> SERVICES
    SERVICES --> API
    API --> MODELS
    API --> SCHEMAS
    API --> AGENTS
    AGENTS --> SERVICES_B
    MODELS --> DB
```

---

## 2. Frontend Component Hierarchy

```mermaid
graph TD
    App["App.tsx<br/>Router Config"]
    
    subgraph Public["Public Routes"]
        Landing["LandingPage.tsx"]
        Login["LoginPage.tsx"]
    end
    
    subgraph User["User Routes (Protected)"]
        UserLayout["UserLayout"]
        Chat["AIChatIntake.tsx"]
        History["UserComplaintHistory.tsx"]
    end
    
    subgraph Admin["Admin Routes (Protected)"]
        AdminLayout["AdminLayout"]
        Dashboard["AdminDashboard.tsx"]
        Console["AdminComplaintConsole.tsx"]
        Provider["ProviderSelection.tsx"]
    end
    
    App --> Public
    App --> User
    App --> Admin
    
    User --> UserLayout
    UserLayout --> Chat
    UserLayout --> History
    
    Admin --> AdminLayout
    AdminLayout --> Dashboard
    AdminLayout --> Console
    Console --> Provider
```

---

## 3. Backend API Routes

```mermaid
graph LR
    main["main.py<br/>FastAPI App"]
    
    subgraph Routes["API Routes"]
        auth["auth.py<br/>/auth/*"]
        users["users.py<br/>/user/*"]
        admin["admin.py<br/>/admin/*"]
        providers["providers.py<br/>/providers/*"]
        chat["chat.py<br/>/user/chat/*"]
    end
    
    subgraph Models["Data Models"]
        user["user.py"]
        complaint["complaint.py"]
        provider["provider.py"]
        timeline["timeline.py"]
    end
    
    main --> Routes
    Routes --> Models
```

---

## 4. Agent System (AI Pipeline)

```mermaid
flowchart TB
    Pipeline["pipeline.py<br/>Orchestrator"]

    subgraph Input["Input Understanding Agent"]
        IU1["Parse Complaint Text"]
        IU2["Extract Entities"]
        IU3["Classify Category"]
    end
    
    subgraph Priority["Prioritization Agent"]
        P1["Calculate Urgency Score"]
        P2["Determine Category Priority"]
        P3["Assign Initial Priority"]
    end
    
    subgraph Assignment["Assignment Agent"]
        A1["Find Available Providers"]
        A2["Match Skills to Category"]
        A3["Assign to Provider"]
    end
    
    subgraph LLM["SARVAM LLM"]
        LLM["sarvam_llm.py<br/>AI Processing"]
    end
    
    Pipeline --> Input
    Pipeline --> Priority
    Pipeline --> Assignment

    IU1 --> IU2 --> IU3
    IU3 --> P1 --> P2 --> P3
    P3 --> A1 --> A2 --> A3
    IU3 --> LLM
```

---

## 5. File Dependency Map

```mermaid
graph TB
    subgraph Frontend["Frontend Dependencies"]
        main_tsx["main.tsx"] --> App_tsx["App.tsx"]
        App_tsx --> ProtectedRoute["ProtectedRoute.tsx"]
        App_tsx --> LandingPage["LandingPage.tsx"]
        App_tsx --> LoginPage["LoginPage.tsx"]
        App_tsx --> UserLayout["UserLayout.tsx"]
        App_tsx --> AdminLayout["AdminLayout.tsx"]
        
        UserLayout --> Navbar["Navbar.tsx"]
        AdminLayout --> Navbar
        
        LandingPage --> Hero["Hero.tsx"]
        LandingPage --> Capabilities["Capabilities.tsx"]
        LandingPage --> Lifecycle["Lifecycle.tsx"]
        LandingPage --> Obstacles["Obstacles.tsx"]
        LandingPage --> Protocol["Protocol.tsx"]
        
        LoginPage --> useAuth["useAuth.ts"]
        useAuth --> authService["authService.ts"]
        
        Chat --> useComplaints["useComplaints.ts"]
        History --> useComplaints
        Console --> useComplaints
        
        useComplaints --> complaintService["complaintService.ts"]
        useAuth --> adminService["adminService.ts"]
        
        complaintService --> api["api.ts"]
        authService --> api
        adminService --> api
    end
```

---

## 6. Key Service Connections

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant API
    participant Auth
    participant DB
    
    User->>UI: Login
    UI->>API: POST /auth/login
    API->>Auth: Validate credentials
    Auth->>DB: Check user
    
    DB-->>Auth: User data
    Auth-->>API: JWT token
    API-->>UI: Response
    
    User->>UI: Submit Complaint
    UI->>API: POST /user/complaints
    API->>DB: Save complaint
    
    API->>Agent: Process complaint
    Agent->>API: Priority & Assignment
    
    DB-->>API: Confirm
    API-->>UI: Success
    
    Admin->>UI: View Complaints
    UI->>API: GET /admin/complaints
    API->>DB: Fetch complaints
    DB-->>API: Data
    API-->>UI: Display
```

---

## 7. Database Models

```mermaid
erDiagram
    USER ||--o{ COMPLAINT : submits
    USER ||--o{ TIMELINE : creates
    PROVIDER ||--o{ COMPLAINT : handles
    COMPLAINT ||--o{ TIMELINE : has
    
    USER {
        string id PK
        string email
        string password_hash
        string name
        string role
        datetime created_at
    }
    
    PROVIDER {
        string id PK
        string name
        string email
        string phone
        string category
        array skills
        string status
        float rating
    }
    
    COMPLAINT {
        string id PK
        string user_id FK
        string provider_id FK
        string title
        string description
        string category
        string status
        int priority
        string location
        array attachments
        datetime created_at
        datetime updated_at
    }
    
    TIMELINE {
        string id PK
        string complaint_id FK
        string user_id FK
        string action
        string description
        datetime timestamp
    }
```

---

## 8. Tech Stack Summary

| Layer | Technology | Files |
|-------|------------|-------|
| **Frontend Framework** | React 18 + TypeScript | `src/main.tsx`, `src/App.tsx` |
| **Build Tool** | Vite | `vite.config.ts` |
| **Routing** | React Router v6 | `App.tsx` |
| **Styling** | Tailwind CSS | `tailwind.config.js`, `src/index.css` |
| **HTTP Client** | Axios | `src/services/api.ts` |
| **Backend Framework** | FastAPI | `backend/app/main.py` |
| **Database** | MongoDB | `backend/app/database.py` |
| **Authentication** | JWT | `backend/app/utils/security.py` |
| **AI Agents** | Custom Python | `backend/app/agents/*` |
| **LLM Integration** | SARVAM API | `backend/app/agents/sarvam_llm.py` |

---

## 9. Critical Code Paths

### Authentication Flow
```
src/pages/LoginPage.tsx
  → src/hooks/useAuth.ts
    → src/services/authService.ts
      → src/services/api.ts (axios instance)
        → backend/app/api/routes/auth.py
          → backend/app/utils/security.py (JWT)
            → backend/app/models/user.py
```

### Complaint Submission
```
src/pages/AIChatIntake.tsx
  → src/hooks/useComplaints.ts
    → src/services/complaintService.ts
      → backend/app/api/routes/users.py
        → backend/app/models/complaint.py
          → backend/app/agents/* (AI processing)
```

### Admin Dashboard
```
src/pages/AdminDashboard.tsx
  → src/hooks/useComplaints.ts
    → src/services/adminService.ts
      → backend/app/api/routes/admin.py
        → backend/app/models/complaint.py
          → backend/app/models/timeline.py
```