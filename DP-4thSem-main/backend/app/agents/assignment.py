"""Assignment Agent — AI-powered provider matching.

This agent selects the best service provider for a given complaint
based on:
- Category match (service_types vs complaint category)
- Service area coverage
- Provider rating and availability
- Price range preference
- Response time urgency

Uses Sarvam AI to generate reasoning when available,
otherwise pure deterministic scoring.
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional

from app.agents.sarvam_llm import sarvam_chat
from app.database import providers_collection

logger = logging.getLogger(__name__)

# Category → service type mapping
CATEGORY_SERVICE_MAP = {
    "electricity": ["electrical", "electrician", "wiring", "appliance_repair"],
    "water": ["plumbing", "water_heater", "water"],
    "plumbing": ["plumbing", "pipe_repair", "leak", "drain_cleaning"],
    "sanitation": ["cleaning", "sanitation", "drain_cleaning"],
    "hvac": ["hvac", "ac_repair", "heating", "cooling"],
    "maintenance": ["maintenance", "handyman", "repairs", "general"],
    "security": ["security", "locksmith", "cctv"],
}

ASSIGNMENT_SYSTEM_PROMPT = """You are an AI assistant for a Smart Complaint Management System.
Given a complaint and a list of available service providers, recommend the best provider.

Respond ONLY with valid JSON (no markdown, no explanation), using this schema:
{
  "recommended_provider_id": "the _id of the best provider",
  "confidence": 0.0 to 1.0,
  "reasoning": "brief explanation of why this provider was chosen",
  "estimated_time": "estimated resolution time like '2-4 hours'",
  "alternatives": ["id1", "id2"]
}"""


def _score_provider(provider: Dict, complaint: Dict) -> float:
    """Score a provider for a complaint using deterministic rules."""
    score = 0.0

    # 1. Service type match (40%)
    complaint_cat = complaint.get("category", "").lower()
    target_types = CATEGORY_SERVICE_MAP.get(complaint_cat, [])
    provider_types = [t.lower() for t in provider.get("service_types", [])]

    type_match = sum(1 for t in target_types if t in provider_types)
    if type_match > 0:
        score += 0.4 * min(type_match / max(len(target_types), 1), 1.0)

    # 2. Rating (25%)
    rating = provider.get("rating", 0)
    score += 0.25 * (rating / 5.0)

    # 3. Availability (20%)
    avail = provider.get("availability_status", "unavailable")
    if avail == "available":
        score += 0.20
    elif avail == "busy":
        score += 0.05

    # 4. Response time (10%) — lower is better
    response_time = provider.get("avg_response_time", 120)
    if response_time <= 30:
        score += 0.10
    elif response_time <= 60:
        score += 0.07
    elif response_time <= 90:
        score += 0.04

    # 5. Area match (5%)
    complaint_area = complaint.get("location", "")
    user_address = complaint.get("user", {}).get("address", {})
    pincode = user_address.get("pincode", "")
    area = user_address.get("area", "")
    service_areas = provider.get("service_areas", [])

    if pincode and pincode in service_areas:
        score += 0.05
    elif area and area in service_areas:
        score += 0.03

    return round(score, 4)


async def find_best_provider(complaint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Find the best service provider for a complaint.
    Uses AI reasoning when available, deterministic scoring as fallback.
    """
    category = complaint.get("category", "").lower()
    target_types = CATEGORY_SERVICE_MAP.get(category, [])

    # Fetch eligible providers from MongoDB
    query = {"is_active": True}
    if target_types:
        query["service_types"] = {"$in": target_types}

    providers = []
    cursor = providers_collection().find(query)
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        providers.append(doc)

    if not providers:
        # Broaden search — get all active providers
        cursor = providers_collection().find({"is_active": True})
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            providers.append(doc)

    if not providers:
        return {
            "recommended_provider_id": None,
            "confidence": 0.0,
            "reasoning": "No providers available",
            "estimated_time": None,
            "alternatives": [],
            "source": "none",
        }

    # Score all providers deterministically
    scored = []
    for p in providers:
        s = _score_provider(p, complaint)
        scored.append((p, s))

    scored.sort(key=lambda x: x[1], reverse=True)
    best = scored[0]
    alternatives = [s[0]["_id"] for s in scored[1:3]]

    # Try AI-enhanced reasoning
    ai_reasoning = None
    try:
        provider_summaries = []
        for p, s in scored[:5]:
            provider_summaries.append(
                f"ID: {p['_id']}, Name: {p['name']}, Platform: {p.get('platform','')}, "
                f"Rating: {p.get('rating',0)}, Response: {p.get('avg_response_time','?')}min, "
                f"Types: {p.get('service_types',[])}, Score: {s}"
            )

        complaint_summary = (
            f"Category: {category}, "
            f"Priority: {complaint.get('priority_level', 'medium')}, "
            f"Description: {complaint.get('description', '')[:200]}, "
            f"Location: {complaint.get('location', '')}"
        )

        ai_response = await sarvam_chat(
            messages=[
                {"role": "system", "content": ASSIGNMENT_SYSTEM_PROMPT},
                {"role": "user", "content": (
                    f"Complaint:\n{complaint_summary}\n\n"
                    f"Available providers (ranked by score):\n" +
                    "\n".join(provider_summaries)
                )},
            ],
            temperature=0.1,
            max_tokens=256,
        )

        if ai_response:
            json_match = re.search(r'\{[^{}]*\}', ai_response, re.DOTALL)
            if json_match:
                ai_result = json.loads(json_match.group())
                ai_reasoning = ai_result.get("reasoning", "")
    except Exception as e:
        logger.warning(f"AI provider reasoning failed: {e}")

    # Priority-based time estimation
    priority = complaint.get("priority_level", "medium")
    time_estimates = {
        "critical": "1-2 hours",
        "high": "2-4 hours",
        "medium": "4-8 hours",
        "low": "1-2 days",
    }

    return {
        "recommended_provider_id": best[0]["_id"],
        "recommended_provider_name": best[0].get("name", ""),
        "recommended_provider_platform": best[0].get("platform", ""),
        "confidence": min(best[1] * 1.2, 1.0),  # Scale up slightly
        "reasoning": ai_reasoning or (
            f"Best match: {best[0].get('name','')} "
            f"(★{best[0].get('rating',0)}, {best[0].get('platform','')}) — "
            f"matched {category} service types with score {best[1]}"
        ),
        "estimated_time": time_estimates.get(priority, "4-8 hours"),
        "alternatives": alternatives,
        "booking_url": best[0].get("deep_link_template", ""),
        "source": "sarvam_ai" if ai_reasoning else "deterministic",
    }
