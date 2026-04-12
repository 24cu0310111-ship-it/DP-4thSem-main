"""Prioritization Agent using LangChain."""

from enum import Enum
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class PriorityLevel(str, Enum):
    """Priority levels for complaints."""

    CRITICAL = "critical"  # Response within 1 hour
    HIGH = "high"  # Response within 4 hours
    MEDIUM = "medium"  # Response within 24 hours
    LOW = "low"  # Response within 72 hours


class PrioritizedComplaint(BaseModel):
    """Prioritized complaint with scoring breakdown."""

    complaint_id: str
    priority_level: PriorityLevel
    priority_score: float = Field(description="Calculated priority score 0-100")
    category_weight: float = Field(description="Weight based on category criticality")
    safety_score: float = Field(description="Safety risk score 0-1")
    urgency_score: float = Field(description="Time sensitivity score 0-1")
    affected_users_score: float = Field(description="Score based on number of affected users")
    sentiment_score: float = Field(description="User frustration level 0-1")
    reasoning: str = Field(
        description="Human-readable explanation of priority decision"
    )
    suggested_response_time: str = Field(
        description="Suggested maximum response time (e.g., '1 hour', '24 hours')"
    )
    escalation_required: bool = Field(
        description="Whether this complaint requires admin escalation"
    )


# Category weights for priority calculation
CATEGORY_WEIGHTS = {
    "electricity": 1.0,
    "water": 0.9,
    "sanitation": 0.85,
    "plumbing": 0.8,
    "security": 0.7,
    "hvac": 0.5,
    "maintenance": 0.3,
    "other": 0.2,
}

# Priority thresholds
PRIORITY_THRESHOLDS = {
    "critical": 80,
    "high": 60,
    "medium": 40,
    "low": 0,
}

# Response time suggestions
RESPONSE_TIMES = {
    "critical": "1 hour",
    "high": "4 hours",
    "medium": "24 hours",
    "low": "72 hours",
}

prioritization_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a complaint prioritization agent for urban services.
Your task is to assign priority levels to complaints based on multiple factors.

PRIORITY CALCULATION FACTORS:

1. CATEGORY CRITICALITY (30% weight):
   - CRITICAL (1.0): Electrical hazards, gas leaks, structural damage
   - HIGH (0.8-0.9): No water, no electricity, blocked toilets
   - MEDIUM (0.5-0.7): AC failure, minor leaks, appliance issues
   - LOW (0.2-0.4): Cosmetic issues, general maintenance

2. SAFETY RISK (25% weight):
   - Any risk to human safety = automatic HIGH minimum priority
   - Electrical hazards, gas leaks, fire risks = CRITICAL
   - Score: 1.0 if safety risk, 0.0 otherwise

3. URGENCY (20% weight):
   - Immediate threat = 1.0 (CRITICAL)
   - Within 24 hours needed = 0.7 (HIGH)
   - Within week acceptable = 0.4 (MEDIUM)
   - No rush = 0.2 (LOW)

4. AFFECTED USERS (15% weight):
   - Entire building = 1.0 (consider escalation)
   - Multiple units = 0.7
   - Single unit = 0.4

5. SENTIMENT/FRUSTRATION (10% weight):
   - High frustration = 1.0 (consider escalation)
   - Medium frustration = 0.5
   - Low frustration = 0.2

WEIGHTED SCORE CALCULATION:
score = (category_weight * 0.30) + (safety_score * 0.25) + (urgency_score * 0.20) + (affected_users_score * 0.15) + (sentiment_score * 0.10)
Then multiply by 100 for final 0-100 score.

PRIORITY LEVELS:
- CRITICAL: score >= 80 (respond within 1 hour)
- HIGH: score >= 60 (respond within 4 hours)
- MEDIUM: score >= 40 (respond within 24 hours)
- LOW: score < 40 (respond within 72 hours)

ESCALATION:
Mark escalation_required = true if:
- Safety risk is present
- Entire building affected
- Critical priority with high sentiment
- Already escalated before

Provide clear, human-readable reasoning for your priority decision.
Be fair and consistent like a human administrator would be.

{format_instructions}
"""),
    ("human", """
Complaint Analysis:
- Category: {category}
- Subcategory: {subcategory}
- Description: {description}
- Safety Risk Identified: {safety_risk}
- Severity Indicators: {severity_indicators}
- Urgency Keywords: {urgency_keywords}
- Affected Users: {affected_users}
- Sentiment Score: {sentiment_score}
- Detected Language: {detected_language}
"""),
])


def determine_priority_level(score: float) -> PriorityLevel:
    """Determine priority level based on score."""
    if score >= PRIORITY_THRESHOLDS["critical"]:
        return PriorityLevel.CRITICAL
    elif score >= PRIORITY_THRESHOLDS["high"]:
        return PriorityLevel.HIGH
    elif score >= PRIORITY_THRESHOLDS["medium"]:
        return PriorityLevel.MEDIUM
    else:
        return PriorityLevel.LOW


def create_prioritization_chain(llm):
    """
    Create the prioritization chain.

    Args:
        llm: LangChain LLM instance

    Returns:
        Runnable chain for prioritizing complaints
    """
    parser = PydanticOutputParser(pydantic_object=PrioritizedComplaint)

    chain = (
        prioritization_prompt
        | llm
        | parser
    )

    return chain


def calculate_priority_score(
    category: str,
    safety_risk: bool,
    urgency_keywords: list,
    affected_users: str,
    sentiment_score: float,
) -> dict:
    """
    Calculate priority score using weighted formula.

    This is a deterministic fallback or validation for the AI-based prioritization.

    Args:
        category: Complaint category
        safety_risk: Whether safety risk exists
        urgency_keywords: List of urgency-related keywords
        affected_users: Scope of affected users
        sentiment_score: User frustration 0-1

    Returns:
        Dictionary with score breakdown and final score
    """
    # Category weight
    category_weight = CATEGORY_WEIGHTS.get(category.lower(), 0.2)

    # Safety score (binary)
    safety_score = 1.0 if safety_risk else 0.0

    # Urgency score based on keywords
    urgency_keywords_high = [
        "urgent", "immediately", "emergency", "right now",
        "तुरंत", "जल्दी", "आपातकालीन",  # Hindi urgency words
        "அவசரம்", "உடனடியாக",  # Tamil
    ]
    urgency_keywords_medium = [
        "soon", "today", "asap", "quickly",
        "जल्द", "आज",  # Hindi
    ]

    urgency_score = 0.2  # Default low
    if any(kw in urgency_keywords for kw in urgency_keywords_high):
        urgency_score = 1.0
    elif any(kw in urgency_keywords for kw in urgency_keywords_medium):
        urgency_score = 0.7
    elif len(urgency_keywords) > 0:
        urgency_score = 0.4

    # Affected users score
    affected_users_score = 0.4  # Default single
    if affected_users.lower() == "building":
        affected_users_score = 1.0
    elif affected_users.lower() == "multiple":
        affected_users_score = 0.7

    # Weighted calculation
    final_score = (
        category_weight * 0.30 +
        safety_score * 0.25 +
        urgency_score * 0.20 +
        affected_users_score * 0.15 +
        sentiment_score * 0.10
    ) * 100

    priority_level = determine_priority_level(final_score)

    return {
        "score": round(final_score, 2),
        "priority_level": priority_level.value,
        "category_weight": category_weight,
        "safety_score": safety_score,
        "urgency_score": urgency_score,
        "affected_users_score": affected_users_score,
        "sentiment_score": sentiment_score,
        "response_time": RESPONSE_TIMES[priority_level.value],
    }


# Example usage
if __name__ == "__main__":
    # Test the deterministic calculation
    result = calculate_priority_score(
        category="electricity",
        safety_risk=False,
        urgency_keywords=["urgent", "immediately"],
        affected_users="building",
        sentiment_score=0.8,
    )
    print(result)
    # Expected: High priority due to building-wide electricity issue
