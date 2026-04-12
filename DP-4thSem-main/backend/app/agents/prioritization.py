"""Prioritization Agent — deterministic scoring with optional AI enhancement.

This module provides the core priority scoring logic used when new complaints
are created. It uses a weighted formula based on category, safety, urgency,
affected users, and sentiment. The AI-based LangChain chain is optional and
requires a Sarvam AI API key.
"""

from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

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

# Urgency keyword sets
URGENCY_HIGH = {
    "urgent", "immediately", "emergency", "right now", "asap", "critical",
    "danger", "fire", "flood", "sparking", "gas leak",
    "तुरंत", "जल्दी", "आपातकालीन",  # Hindi
    "அவசரம்", "உடனடியாக",  # Tamil
}

URGENCY_MEDIUM = {
    "soon", "today", "quickly", "fast",
    "जल्द", "आज",  # Hindi
}

# Safety keywords that auto-elevate priority
SAFETY_KEYWORDS = {
    "fire", "smoke", "sparking", "exposed wire", "gas leak", "gas smell",
    "flood", "flooding", "collapse", "crack", "structural",
    "electric shock", "electrocution", "burning",
}


def determine_priority_level(score: float) -> str:
    """Determine priority level based on score."""
    if score >= PRIORITY_THRESHOLDS["critical"]:
        return "critical"
    elif score >= PRIORITY_THRESHOLDS["high"]:
        return "high"
    elif score >= PRIORITY_THRESHOLDS["medium"]:
        return "medium"
    else:
        return "low"


def detect_safety_risk(description: str) -> bool:
    """Check if the description contains safety risk indicators."""
    desc_lower = description.lower()
    return any(keyword in desc_lower for keyword in SAFETY_KEYWORDS)


def extract_urgency_keywords(description: str) -> List[str]:
    """Extract urgency keywords from description."""
    desc_lower = description.lower()
    found = []
    for kw in URGENCY_HIGH:
        if kw in desc_lower:
            found.append(kw)
    for kw in URGENCY_MEDIUM:
        if kw in desc_lower:
            found.append(kw)
    return found


def calculate_priority_score(
    category: str,
    safety_risk: bool,
    urgency_keywords: List[str],
    affected_users: str,
    sentiment_score: float,
    description: str = "",
) -> Dict[str, Any]:
    """
    Calculate priority score using weighted formula.

    This is the deterministic scoring engine. It runs even if AI agents fail.
    """
    # Auto-detect safety from description if not explicitly set
    if description and not safety_risk:
        safety_risk = detect_safety_risk(description)

    # Auto-extract urgency keywords if none provided
    if description and not urgency_keywords:
        urgency_keywords = extract_urgency_keywords(description)

    # Category weight (30%)
    category_weight = CATEGORY_WEIGHTS.get(category.lower(), 0.2)

    # Safety score (25%) — binary
    safety_score = 1.0 if safety_risk else 0.0

    # Urgency score (20%)
    urgency_score = 0.2  # Default low
    if any(kw in URGENCY_HIGH for kw in urgency_keywords):
        urgency_score = 1.0
    elif any(kw in URGENCY_MEDIUM for kw in urgency_keywords):
        urgency_score = 0.7
    elif len(urgency_keywords) > 0:
        urgency_score = 0.4

    # Affected users score (15%)
    affected_users_score = 0.4  # Default single
    if affected_users.lower() == "building":
        affected_users_score = 1.0
    elif affected_users.lower() == "multiple":
        affected_users_score = 0.7

    # Weighted calculation
    final_score = (
        category_weight * 0.30
        + safety_score * 0.25
        + urgency_score * 0.20
        + affected_users_score * 0.15
        + sentiment_score * 0.10
    ) * 100

    priority_level = determine_priority_level(final_score)

    # Generate reasoning
    reasons = []
    if safety_risk:
        reasons.append("Safety risk detected")
    reasons.append(f"Category: {category} (weight: {category_weight})")
    if urgency_keywords:
        reasons.append(f"Urgency indicators: {', '.join(urgency_keywords[:3])}")
    if affected_users.lower() in ("building", "multiple"):
        reasons.append(f"Affects {affected_users} users")

    reasoning = ". ".join(reasons) + f". Overall score: {round(final_score, 1)}/100."

    return {
        "score": round(final_score, 2),
        "priority_level": priority_level,
        "category_weight": category_weight,
        "safety_score": safety_score,
        "urgency_score": urgency_score,
        "affected_users_score": affected_users_score,
        "sentiment_score": sentiment_score,
        "response_time": RESPONSE_TIMES[priority_level],
        "reasoning": reasoning,
    }
