# AI Agent Design with LangChain + Sarvam AI

## Overview
This document details the LangChain AI agents used for natural language understanding, multimedia processing, and intelligent prioritization.

---

## 1. Input Understanding Agent

### Purpose
Process multi-modal user inputs (text, image, voice) to extract structured complaint information.

### LangChain Components Used

```python
# Core Components
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# Sarvam AI Integration (via custom wrapper or API)
from langchain_community.llms import SarvamAI  # or custom implementation
```

### Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   INPUT UNDERSTANDING AGENT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Text      │    │   Image     │    │   Voice     │         │
│  │   Input     │    │   Input     │    │   Input     │         │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘         │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              Multi-modal Fusion Layer                │       │
│  │         (LangChain RunnableParallel)                 │       │
│  └─────────────────────┬───────────────────────────────┘       │
│                        │                                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────┐       │
│  │           Sarvam AI NLU Processing                   │       │
│  │   - Entity Extraction (location, item, issue)        │       │
│  │   - Intent Classification                            │       │
│  │   - Sentiment Analysis                               │       │
│  │   - Language Detection (Indian languages support)    │       │
│  └─────────────────────┬───────────────────────────────┘       │
│                        │                                        │
│                        ▼                                        │
│  ┌─────────────────────────────────────────────────────┐       │
│  │           Structured Output Parser                   │       │
│  │   Pydantic model: ComplaintInput                     │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
# backend/app/agents/input_understanding.py

from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableParallel

# Output schema
class ComplaintInput(BaseModel):
    """Structured complaint input extracted from user message"""
    category: str = Field(description="Problem category: electricity, water, sanitation, hvac, plumbing, maintenance, security, other")
    subcategory: str = Field(description="Specific sub-category")
    location: str = Field(description="Exact location of the issue")
    description: str = Field(description="Detailed description of the problem")
    severity_indicators: List[str] = Field(description="Key phrases indicating severity")
    urgency_keywords: List[str] = Field(description="Words indicating time sensitivity")
    affected_users: str = Field(description="Number of people affected: single, multiple, building")
    safety_risk: bool = Field(description="Whether there's a safety hazard")
    media_analysis: Optional[str] = Field(description="Analysis of attached images/audio")
    detected_language: str = Field(description="Language detected in user input")
    sentiment_score: float = Field(description="User frustration level 0-1")

# Prompt template optimized for Sarvam AI
input_understanding_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an intelligent complaint understanding agent for urban services.
    Analyze the user's complaint and extract structured information.
    
    You are powered by Sarvam AI, optimized for Indian languages and context.
    
    Consider these priority indicators:
    - SAFETY RISK: Electrical hazards, gas leaks, fire risks = CRITICAL
    - BASIC NECESSITY: No water, no electricity, blocked toilet = HIGH
    - COMFORT: AC not working, minor leaks = MEDIUM  
    - COSMETIC: Paint peeling, minor scratches = LOW
    
    Extract entities, intent, and severity from the user's description.
    Support Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, and English.
    
    {format_instructions}
    """),
    ("human", "{user_input}"),
    ("human", "Attached media: {media_context}"),
])

# Parser
parser = PydanticOutputParser(pydantic_object=ComplaintInput)

# Chain construction
def create_input_understanding_chain(llm):
    return (
        RunnableParallel({
            "user_input": lambda x: x["user_input"],
            "media_context": lambda x: x.get("media_context", "No media attached"),
            "format_instructions": lambda x: parser.get_format_instructions()
        })
        | input_understanding_prompt
        | llm
        | parser
    )
```

### Multimedia Processing

```python
# Image Analysis Chain
from langchain_core.runnables import RunnableLambda
import base64

def analyze_image(image_data: bytes) -> str:
    """Analyze complaint-related images using vision model"""
    # Use Sarvam AI vision or integrate with another vision API
    # Return structured analysis
    return "Image shows water leakage from ceiling pipe, moderate flow rate"

def transcribe_audio(audio_data: bytes) -> str:
    """Transcribe voice complaints using Sarvam AI speech-to-text"""
    # Sarvam AI supports Indian language speech recognition
    return "पानी की पाइप लीक हो रही है"  # Example Hindi transcription

# Multi-modal runnable
multimodal_chain = RunnableParallel({
    "text_analysis": input_understanding_chain,
    "image_analysis": RunnableLambda(lambda x: analyze_image(x["image"])) if x.get("image") else lambda x: "No image",
    "audio_transcription": RunnableLambda(lambda x: transcribe_audio(x["audio"])) if x.get("audio") else lambda x: "No audio",
})
```

---

## 2. Prioritization Agent

### Purpose
Assign priority scores to complaints based on extracted information.

### Priority Matrix

| Factor | Weight | Scores |
|--------|--------|--------|
| Category Criticality | 30% | Electricity(1.0), Water(0.9), Sanitation(0.8), HVAC(0.5), Maintenance(0.3) |
| Safety Risk | 25% | Yes(1.0), No(0.0) |
| Urgency Level | 20% | Immediate(1.0), 24h(0.7), Week(0.4), Flexible(0.2) |
| Affected Users | 15% | Building(1.0), Multiple(0.7), Single(0.4) |
| Sentiment/Frustration | 10% | High(1.0), Medium(0.5), Low(0.2) |

### Implementation

```python
# backend/app/agents/prioritization.py

from enum import Enum
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class PriorityLevel(str, Enum):
    CRITICAL = "critical"      # Response within 1 hour
    HIGH = "high"              # Response within 4 hours
    MEDIUM = "medium"          # Response within 24 hours
    LOW = "low"                # Response within 72 hours

class PrioritizedComplaint(BaseModel):
    """Prioritized complaint with scoring breakdown"""
    complaint_id: str
    priority_level: PriorityLevel
    priority_score: float = Field(description="0-100 score")
    category_weight: float
    safety_score: float
    urgency_score: float
    affected_users_score: float
    sentiment_score: float
    reasoning: str = Field(description="Human-readable explanation of priority decision")
    suggested_response_time: str
    escalation_required: bool = Field(description="Whether admin escalation is needed")

prioritization_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a complaint prioritization agent.
    Assign priority levels based on:
    
    1. CATEGORY CRITICALITY (30%):
       - CRITICAL: Electrical hazards, gas leaks, structural damage
       - HIGH: No water, no electricity, blocked toilets
       - MEDIUM: AC failure, minor leaks, appliance issues
       - LOW: Cosmetic issues, general maintenance
    
    2. SAFETY RISK (25%):
       - Any risk to human safety = automatic HIGH minimum
    
    3. URGENCY (20%):
       - Immediate threat = CRITICAL
       - Within 24 hours = HIGH
       - Within week = MEDIUM
       - No rush = LOW
    
    4. AFFECTED USERS (15%):
       - Entire building = escalate
       - Multiple units = HIGH
       - Single unit = based on other factors
    
    5. SENTIMENT (10%):
       - High frustration = consider escalation
    
    Provide clear reasoning for your priority decision.
    Be fair and consistent like a human administrator.
    
    {format_instructions}
    """),
    ("human", """
    Complaint Details:
    Category: {category}
    Subcategory: {subcategory}
    Description: {description}
    Safety Risk: {safety_risk}
    Severity Indicators: {severity_indicators}
    Urgency Keywords: {urgency_keywords}
    Affected Users: {affected_users}
    Sentiment Score: {sentiment_score}
    """),
])

def create_prioritization_chain(llm):
    parser = PydanticOutputParser(pydantic_object=PrioritizedComplaint)
    
    return (
        prioritization_prompt
        | llm
        | parser
    )

def calculate_priority_score(prioritized: PrioritizedComplaint) -> dict:
    """Calculate weighted priority score"""
    weights = {
        "category": 0.30,
        "safety": 0.25,
        "urgency": 0.20,
        "affected_users": 0.15,
        "sentiment": 0.10
    }
    
    score = (
        prioritized.category_weight * weights["category"] +
        prioritized.safety_score * weights["safety"] +
        prioritized.urgency_score * weights["urgency"] +
        prioritized.affected_users_score * weights["affected_users"] +
        prioritized.sentiment_score * weights["sentiment"]
    ) * 100
    
    return {
        "score": round(score, 2),
        "level": prioritized.priority_level.value,
        "reasoning": prioritized.reasoning
    }
```

---

## 3. Assignment Agent

### Purpose
Match complaints to appropriate service providers from integrated platforms.

### Implementation

```python
# backend/app/agents/assignment.py

from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class ServiceProvider(BaseModel):
    """Service provider from external platform"""
    platform: str  # Urban Company, TaskRabbit, Handy, etc.
    provider_name: str
    service_type: str
    rating: float
    reviews_count: int
    price_range: str  # $, $$, $$$
    estimated_price: Optional[float]
    availability: str  # Available, Next Day, 2-3 days
    distance_km: float
    platform_icon: str  # URL to platform logo
    deep_link: str  # Direct booking URL

class AssignmentRecommendation(BaseModel):
    """Recommended service providers for a complaint"""
    complaint_id: str
    category: str
    location: str
    recommended_providers: List[ServiceProvider]
    best_match_reason: str
    filters_applied: dict

assignment_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a service provider matching agent.
    Based on the complaint category and location, recommend suitable service providers.
    
    Available platforms:
    - Urban Company: Home services, repairs, maintenance
    - TaskRabbit: Task-based services, handyman
    - Handy: Cleaning, home services
    - Local providers: Area-specific services
    
    Consider:
    1. Service type match
    2. Location coverage
    3. Price range
    4. Availability
    5. Ratings and reviews
    
    Return top 5 providers sorted by relevance.
    
    {format_instructions}
    """),
    ("human", """
    Complaint Category: {category}
    Subcategory: {subcategory}
    Location: {location}
    Priority Level: {priority_level}
    """),
])

def create_assignment_chain(llm, provider_database):
    """Create assignment chain with provider database context"""
    
    def inject_providers(x):
        # Query provider database based on category and location
        providers = provider_database.query(
            category=x["category"],
            location=x["location"]
        )
        return {**x, "available_providers": providers}
    
    return (
        RunnableParallel({
            "category": lambda x: x["category"],
            "subcategory": lambda x: x["subcategory"],
            "location": lambda x: x["location"],
            "priority_level": lambda x: x["priority_level"],
            "available_providers": inject_providers
        })
        | assignment_prompt
        | llm
        | PydanticOutputParser(pydantic_object=AssignmentRecommendation)
    )
```

---

## 4. Full Agent Pipeline

```python
# backend/app/agents/pipeline.py

from langchain_core.runnables import RunnableSequence

def create_full_pipeline(llm):
    """Complete complaint processing pipeline"""
    
    return RunnableSequence(
        input_understanding_chain(llm),
        prioritization_chain(llm),
        assignment_chain(llm),
    )

# Usage
async def process_complaint(user_input: str, media: dict, user_location: str):
    """Process a new complaint through the AI pipeline"""
    
    result = await pipeline.ainvoke({
        "user_input": user_input,
        "media_context": media,
        "location": user_location,
    })
    
    return {
        "understanding": result[0],
        "prioritization": result[1],
        "assignment": result[2],
    }
```

---

## Sarvam AI Integration Notes

### API Endpoints
```
Text NLU: POST https://api.sarvam.ai/v1/nlu
Speech-to-Text: POST https://api.sarvam.ai/v1/stt
Image Analysis: POST https://api.sarvam.ai/v1/vision
```

### Supported Languages
- Hindi, Tamil, Telugu, Kannada, Malayalam
- Bengali, Marathi, Gujarati, Punjabi
- English

### Authentication
```python
import os
from sarvam_ai import SarvamAI

client = SarvamAI(api_key=os.getenv("SARVAM_API_KEY"))
```

---

## Testing the Agents

```python
# tests/test_agents.py

async def test_electrical_complaint():
    """Test high-priority electrical complaint"""
    result = await process_complaint(
        user_input="बिजली चली गई है और पूरा बिल्डिंग अंधेरे में है",
        media={},
        user_location="Sector 15, Gurgaon"
    )
    assert result["prioritization"]["priority_level"] == "high"
    assert "building" in result["prioritization"]["reasoning"].lower()

async def test_water_leak_emergency():
    """Test critical water leak with image"""
    with open("test_images/leak.jpg", "rb") as f:
        image_data = f.read()
    
    result = await process_complaint(
        user_input="पाइप फट गया है, पानी हर जगह फैल रहा है!",
        media={"image": image_data},
        user_location="DLF Phase 3"
    )
    assert result["prioritization"]["priority_level"] == "critical"
    assert result["prioritization"]["safety_score"] > 0.8
```
