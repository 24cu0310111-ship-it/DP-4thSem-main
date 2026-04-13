# 🏛️ Smart Complaint Management System (SCMS)

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Sarvam AI](https://img.shields.io/badge/AI-Sarvam_AI-blueviolet?style=for-the-badge)](https://www.sarvam.ai/)

> **SCMS** is an advanced, AI-powered platform designed to revolutionize urban infrastructure management. By leveraging a multi-agent orchestration pipeline, SCMS automates the intake, analysis, prioritization, and assignment of civic complaints (plumbing, electricity, sanitation, etc.), ensuring rapid resolution and transparent tracking.

---

## ✨ Key Features

### 🤖 AI-Powered Complaint Intake
- **Conversational AI Assistant**: Interactive chat interface for detailing issues using natural language.
- **Multi-Agent Pipeline**: 
  - **NLU Agent**: Extracts category, urgency, and safety risks from text.
  - **Prioritization Agent**: Calculates weighted priority scores using a 5-factor formula.
  - **Assignment Agent**: Automatically matches complaints to the best-rated service provider.
- **Multilingual Support**: Supports input in English, Hindi, Tamil, and more via Sarvam AI.

### 📊 Administrative Control
- **Executive Dashboard**: Real-time analytics on resolution times, satisfaction scores, and issue trends.
- **Granular Management**: Admin console for status transitions, manual provider re-assignment, and internal notes.
- **Timeline Tracking**: Immutable audit logs for every action taken on a complaint.

### 📱 User Experience
- **Fluid & Responsive UI**: Built with a sleek, futuristic "Obsidian" design system.
- **History & Tracking**: Real-time updates and escalation paths for citizen-filed complaints.
- **Visual Feedback**: Micro-animations and high-fidelity transitions powered by Framer Motion.

---

## 🏗️ Technical Architecture

### Frontend (Client)
- **Framework**: React + TypeScript + Vite
- **Styling**: Tailwind CSS + Obsidian UI Components
- **State**: React Hooks & Context API

### Backend (API)
- **Framework**: FastAPI (Python)
- **Database**: MongoDB (Motor Async Driver)
- **Security**: JWT Stateless Authentication (OAuth2)
- **Agent Framework**: LangChain + Sarvam AI (`sarvam-m`)

---

## 🚀 Getting Started

### 1. Prerequisites
- **Node.js**: v18+
- **Python**: v3.9+
- **MongoDB**: Running on `localhost:27017`

### 2. Basic Setup

#### Clone & Install
```bash
git clone https://github.com/24cu0310111-ship-it/DP-4thSem-main.git
cd DP-4thSem-main
```

#### Backend Setup
```bash
cd DP-4thSem-main/backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your SARVAM_API_KEY
python seed_data.py  # Seed test users and providers
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd DP-4thSem-main
npm install
npm run dev
```

---

## 📋 Test Credentials

| Role | Username / Phone | Password |
| :--- | :--- | :--- |
| **User** | `+919876543210` | `user123` |
| **Admin** | `admin` | `admin123` |

---

## 🛠️ Project Structure

```text
DP-4thSem-main/
├── DP-4thSem-main/      # Core Application Code
│   ├── backend/         # FastAPI Server & AI Agents
│   │   ├── app/
│   │   │   ├── agents/  # NLU, Prioritization, Pipeline logic
│   │   │   ├── api/     # Routes & Dependencies
│   │   │   └── models/  # MongoDB Schemas
│   ├── src/             # React Frontend
│   │   ├── pages/       # View components
│   │   ├── services/    # API integration
│   │   └── components/  # Atomic UI units
├── implementation_plan.md
└── CONTINUE.md          # Active Project Status
```

---

## ⚖️ License
Copyright © 2026 SCMS Development Team. Built for Advanced Project Excellence.
