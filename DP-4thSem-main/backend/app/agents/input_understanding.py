"""Input Understanding Agent — NLU for complaint text.

This agent analyzes raw complaint descriptions to extract:
- Category classification (electricity, plumbing, water, etc.)
- Subcategory identification
- Urgency level detection
- Safety risk assessment
- Affected scope (single user, multiple, building-wide)
- Sentiment analysis
- Language detection (supports multilingual input via Sarvam AI)

Falls back to keyword-based deterministic logic if AI is unavailable.
"""

import json
import logging
import re
from typing import Dict, Any, Optional

from app.agents.sarvam_llm import sarvam_chat

logger = logging.getLogger(__name__)

# System prompt for Sarvam AI NLU
NLU_SYSTEM_PROMPT = """You are an AI assistant for a Smart Complaint Management System (SCMS).
Analyze the given complaint text and extract structured information.

Respond ONLY with valid JSON (no markdown, no explanation), using this exact schema:
{
  "category": "one of: electricity, water, plumbing, sanitation, hvac, maintenance, security, other",
  "subcategory": "specific issue type like pipe_leak, power_outage, etc.",
  "urgency": "one of: critical, high, medium, low",
  "safety_risk": true or false,
  "affected_scope": "one of: single, multiple, building",
  "sentiment_score": 0.0 to 1.0 (0=calm, 1=very distressed),
  "detected_language": "ISO 639-1 code like en, hi, ta",
  "key_issues": ["list", "of", "main", "issues"],
  "urgency_keywords": ["list", "of", "urgency", "indicators"]
}"""

# Keyword maps for deterministic fallback
CATEGORY_KEYWORDS = {
    "electricity": [
        "electric", "power", "voltage", "current", "wiring", "circuit",
        "breaker", "fuse", "outlet", "switch", "light", "spark", "shock",
        "बिजली", "करंट",  # Hindi
        "மின்சாரம்",  # Tamil
    ],
    "water": [
        "water", "tap", "supply", "tank", "pressure", "contaminated",
        "dirty water", "no water", "water heater", "geyser",
        "पानी", "जल",  # Hindi
        "தண்ணீர்",  # Tamil
    ],
    "plumbing": [
        "plumb", "pipe", "leak", "drain", "clog", "sewage", "toilet",
        "sink", "faucet", "overflow", "flooding",
        "नली", "पाइप",  # Hindi
    ],
    "sanitation": [
        "garbage", "trash", "waste", "cleaning", "hygiene", "pest",
        "cockroach", "rat", "sanitation", "smell", "odor",
        "कूड़ा", "सफाई",  # Hindi
    ],
    "hvac": [
        "ac", "air condition", "heating", "cooling", "ventilation",
        "temperature", "hvac", "thermostat", "fan",
        "एसी",  # Hindi
    ],
    "maintenance": [
        "paint", "wall", "ceiling", "floor", "door", "window",
        "repair", "broken", "crack", "damage", "lift", "elevator",
        "मरम्मत",  # Hindi
    ],
    "security": [
        "security", "lock", "cctv", "camera", "gate", "theft",
        "break-in", "guard", "alarm", "intruder",
        "सुरक्षा", "ताला",  # Hindi
    ],
}

URGENCY_KEYWORDS_HIGH = {
    "urgent", "immediately", "emergency", "right now", "asap", "critical",
    "danger", "fire", "flood", "sparking", "gas leak", "collapse",
    "तुरंत", "जल्दी", "आपातकालीन", "அவசரம்",
}

URGENCY_KEYWORDS_MEDIUM = {
    "soon", "today", "quickly", "fast", "as soon as possible",
    "जल्द", "आज",
}

SAFETY_KEYWORDS = {
    "fire", "smoke", "sparking", "exposed wire", "gas leak", "gas smell",
    "flood", "flooding", "collapse", "crack", "structural",
    "electric shock", "electrocution", "burning", "explosion",
}


def _deterministic_analysis(description: str) -> Dict[str, Any]:
    """Keyword-based fallback when AI is unavailable."""
    desc_lower = description.lower()

    # Detect category
    best_category = "other"
    best_score = 0
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in desc_lower)
        if score > best_score:
            best_score = score
            best_category = cat

    # Detect urgency
    urgency = "medium"
    urgency_kws = []
    for kw in URGENCY_KEYWORDS_HIGH:
        if kw in desc_lower:
            urgency = "high"
            urgency_kws.append(kw)
    if not urgency_kws:
        for kw in URGENCY_KEYWORDS_MEDIUM:
            if kw in desc_lower:
                urgency = "medium"
                urgency_kws.append(kw)

    # Safety risk
    safety_risk = any(kw in desc_lower for kw in SAFETY_KEYWORDS)
    if safety_risk:
        urgency = "critical"

    # Affected scope
    scope = "single"
    if any(w in desc_lower for w in ["building", "all residents", "entire", "floor"]):
        scope = "building"
    elif any(w in desc_lower for w in ["multiple", "several", "neighbors", "units"]):
        scope = "multiple"

    # Basic sentiment (by distress word count)
    distress = ["urgent", "help", "please", "terrible", "worst", "danger", "scared"]
    sentiment = min(sum(0.15 for w in distress if w in desc_lower), 1.0)

    # Language detection (simple)
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', description))
    tamil_chars = len(re.findall(r'[\u0B80-\u0BFF]', description))
    if hindi_chars > 3:
        lang = "hi"
    elif tamil_chars > 3:
        lang = "ta"
    else:
        lang = "en"

    return {
        "category": best_category,
        "subcategory": "",
        "urgency": urgency,
        "safety_risk": safety_risk,
        "affected_scope": scope,
        "sentiment_score": round(sentiment, 2),
        "detected_language": lang,
        "key_issues": [],
        "urgency_keywords": urgency_kws,
        "source": "deterministic",
    }


async def analyze_complaint(description: str) -> Dict[str, Any]:
    """
    Analyze a complaint description using Sarvam AI.
    Falls back to deterministic keyword-based analysis if AI fails.
    """
    # Try AI-based analysis
    try:
        response = await sarvam_chat(
            messages=[
                {"role": "system", "content": NLU_SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this complaint:\n\n{description}"},
            ],
            temperature=0.1,
            max_tokens=512,
        )

        if response:
            # Parse JSON from response
            # Try to extract JSON from the response
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["source"] = "sarvam_ai"
                logger.info(f"AI analysis successful: category={result.get('category')}")
                return result
            else:
                logger.warning("AI response did not contain valid JSON, using fallback")

    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse AI response: {e}")
    except Exception as e:
        logger.warning(f"AI analysis failed: {e}")

    # Fallback to deterministic
    logger.info("Using deterministic complaint analysis")
    return _deterministic_analysis(description)
