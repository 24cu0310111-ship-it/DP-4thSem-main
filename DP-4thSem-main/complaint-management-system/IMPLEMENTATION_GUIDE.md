# Implementation Guide

## Project Overview

This guide helps you implement the Smart Complaint Management System (SCMS) step by step.

---

## Prerequisites

Install these tools before starting:

1. **Python 3.11+** - https://www.python.org/downloads/
2. **Node.js 18+** - https://nodejs.org/
3. **PostgreSQL 15+** - https://www.postgresql.org/download/
4. **Redis 7+** - https://redis.io/download/
5. **MongoDB 6+** - https://www.mongodb.com/try/download/community
6. **Git** - https://git-scm.com/

---

## Step 1: Environment Setup

### 1.1 Create Project Structure

```bash
# Create main directory
mkdir scms
cd scms

# Create subdirectories
mkdir backend frontend docs

# Clone or copy files into appropriate directories
```

### 1.2 Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

### 1.3 Frontend Setup

```bash
cd ../frontend

# Initialize Next.js project (if not already done)
npx create-next-app@latest . --typescript --tailwind --app

# Install additional dependencies
npm install @radix-ui/react-* lucide-react recharts
npm install zustand axios socket.io-client
npm install react-hook-form @hookform/resolvers zod

# Install shadcn/ui
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input dialog table badge
```

---

## Step 2: Configure Environment Variables

### Backend .env file

```env
# Database
DATABASE_URL=postgresql://scms_user:password@localhost:5432/scms_db
MONGODB_URL=mongodb://localhost:27017/scms_db
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=generate-a-secure-random-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Sarvam AI (Get API key from https://sarvam.ai)
SARVAM_API_KEY=your-sarvam-api-key

# AWS S3 (Optional for file storage)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-south-1
AWS_BUCKET_NAME=scms-media

# Optional: Twilio for SMS
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# Optional: SendGrid for Email
SENDGRID_API_KEY=
```

### Generate Secret Key

```python
# Run this in Python to generate a secure key
import secrets
print(secrets.token_urlsafe(32))
```

---

## Step 3: Database Setup

### 3.1 Create PostgreSQL Database

```bash
# Using psql
psql -U postgres

# Inside psql:
CREATE DATABASE scms_db;
CREATE USER scms_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE scms_db TO scms_user;
\q
```

### 3.2 Run Migrations

```bash
cd backend

# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

---

## Step 4: Start Backend Services

### 4.1 Start Redis

```bash
# Windows (if using Redis for Windows)
redis-server

# Linux/Mac
redis-server
```

### 4.2 Start MongoDB

```bash
# Windows (service should auto-start)
# Linux/Mac
mongod
```

### 4.3 Run Backend Server

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4.4 Verify Backend

Open browser: http://localhost:8000/docs

You should see the FastAPI Swagger documentation.

---

## Step 5: Start Frontend

```bash
cd frontend

# Development server
npm run dev

# Production build
npm run build
npm run start
```

Open browser: http://localhost:3000

---

## Step 6: Test the Application

### 6.1 Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+919876543210",
    "email": "test@example.com",
    "name": "Test User",
    "password": "TestPass123!",
    "address": {
      "flat_no": "A-101",
      "building": "Test Apartments",
      "area": "Test Area",
      "city": "Test City",
      "pincode": "122001"
    }
  }'
```

### 6.2 Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+919876543210",
    "password": "TestPass123!"
  }'
```

### 6.3 Register a Complaint

```bash
curl -X POST http://localhost:8000/api/v1/user/complaints \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "category": "plumbing",
    "subcategory": "pipe_leak",
    "description": "Water pipe leaking in kitchen",
    "location": "kitchen sink"
  }'
```

---

## Step 7: Docker Setup (Optional)

### 7.1 Create docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: scms_db
      POSTGRES_USER: scms_user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://scms_user:password@postgres:5432/scms_db
      MONGODB_URL: mongodb://mongodb:27017/scms_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  postgres_data:
  mongodb_data:
```

### 7.2 Run with Docker

```bash
docker-compose up -d
```

---

## Step 8: Sarvam AI Integration

### 8.1 Get API Key

1. Visit https://sarvam.ai
2. Sign up for developer access
3. Get your API key from dashboard

### 8.2 Configure Sarvam Client

Create `backend/app/utils/sarvam_client.py`:

```python
import httpx
from app.config import settings

class SarvamAIClient:
    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.base_url = settings.SARVAM_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def analyze_text(self, text: str, language: str = "hi") -> dict:
        """Analyze text for NLU."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/nlu",
                headers=self.headers,
                json={
                    "text": text,
                    "language": language,
                }
            )
            return response.json()

    async def transcribe_audio(self, audio_data: bytes) -> str:
        """Transcribe audio to text."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/stt",
                headers=self.headers,
                files={"audio": audio_data}
            )
            result = response.json()
            return result.get("text", "")

    async def analyze_image(self, image_data: bytes) -> str:
        """Analyze image content."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/vision",
                headers=self.headers,
                files={"image": image_data},
                data={"prompt": "Describe any damage or issues in this image"}
            )
            result = response.json()
            return result.get("description", "")

# Usage
sarvam_client = SarvamAIClient()
```

---

## Step 9: Testing

### 9.1 Run Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### 9.2 Run Frontend Tests

```bash
cd frontend
npm test
```

---

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Solution: Check DATABASE_URL in .env matches your PostgreSQL credentials
```

**2. Port Already in Use**
```
Solution: Change port in uvicorn command or stop the existing process
Windows: netstat -ano | findstr :8000
         taskkill /PID <PID> /F
Linux/Mac: lsof -i :8000
           kill -9 <PID>
```

**3. Module Not Found**
```
Solution: Ensure virtual environment is activated and requirements installed
pip install -r requirements.txt
```

**4. CORS Error in Frontend**
```
Solution: Check CORS_ORIGINS in backend config includes your frontend URL
```

**5. Sarvam AI API Error**
```
Solution: Verify API key is correct and has credits remaining
```

---

## Next Steps

After basic setup:

1. **Customize UI** - Modify frontend components for your branding
2. **Add More Providers** - Integrate additional service platforms
3. **Configure Notifications** - Set up Twilio/SendGrid for SMS/Email
4. **Deploy to Production** - Use Docker + cloud provider
5. **Monitor & Log** - Set up logging and monitoring tools

---

## Support

For issues or questions:
- Check documentation in `/docs` folder
- Review API spec at http://localhost:8000/docs
- Check logs in backend terminal
