"""AI Pipeline Orchestrator — chains NLU → Prioritization → Assignment.

This module ties together all three AI agents into a single workflow:
1. Input Understanding Agent: analyzes raw complaint text (category, urgency, safety, sentiment)
2. Prioritization Agent: calculates weighted priority score
3. Assignment Agent: finds the best service provider

The pipeline is invoked when a complaint is created or when the chat
assistant needs to analyze a user's message.
"""

import logging
from typing import Dict, Any, Optional

from app.agents.input_understanding import analyze_complaint
from app.agents.prioritization import calculate_priority_score
from app.agents.assignment import find_best_provider

logger = logging.getLogger(__name__)


async def run_complaint_pipeline(
    description: str,
    location: str = "",
    user_info: Optional[Dict[str, Any]] = None,
    category_override: Optional[str] = None,
    skip_assignment: bool = False,
) -> Dict[str, Any]:
    """
    Run the full AI complaint processing pipeline.

    Args:
        description: Raw complaint text from the user.
        location: Location/area of the complaint.
        user_info: Optional dict with user name, phone, address.
        category_override: If provided, use this category instead of AI-detected one.
        skip_assignment: If True, skip provider assignment step (useful for chat preview).

    Returns:
        A unified dict containing:
        - nlu_analysis: full NLU results (category, urgency, safety, sentiment, etc.)
        - priority: priority scoring results (score, level, reasoning)
        - assignment: provider recommendation (or None if skipped)
        - enriched_fields: ready-to-merge fields for the complaint document
    """
    result = {
        "nlu_analysis": None,
        "priority": None,
        "assignment": None,
        "enriched_fields": {},
        "pipeline_status": "started",
        "errors": [],
    }

    # ── Step 1: Input Understanding (NLU) ──────────────────────────────
    logger.info("Pipeline Step 1/3: Running NLU analysis...")
    try:
        nlu = await analyze_complaint(description)
        result["nlu_analysis"] = nlu
        logger.info(
            f"NLU complete: category={nlu.get('category')}, "
            f"urgency={nlu.get('urgency')}, source={nlu.get('source')}"
        )
    except Exception as e:
        logger.error(f"NLU analysis failed: {e}")
        result["errors"].append(f"NLU failed: {str(e)}")
        # Provide minimal fallback
        nlu = {
            "category": category_override or "other",
            "subcategory": "",
            "urgency": "medium",
            "safety_risk": False,
            "affected_scope": "single",
            "sentiment_score": 0.5,
            "detected_language": "en",
            "key_issues": [],
            "urgency_keywords": [],
            "source": "fallback",
        }
        result["nlu_analysis"] = nlu

    # Use category override if provided, otherwise use AI-detected category
    final_category = category_override or nlu.get("category", "other")

    # ── Step 2: Prioritization ─────────────────────────────────────────
    logger.info("Pipeline Step 2/3: Calculating priority...")
    try:
        priority = calculate_priority_score(
            category=final_category,
            safety_risk=nlu.get("safety_risk", False),
            urgency_keywords=nlu.get("urgency_keywords", []),
            affected_users=nlu.get("affected_scope", "single"),
            sentiment_score=nlu.get("sentiment_score", 0.5),
            description=description,
        )
        result["priority"] = priority
        logger.info(
            f"Priority complete: level={priority.get('priority_level')}, "
            f"score={priority.get('score')}"
        )
    except Exception as e:
        logger.error(f"Prioritization failed: {e}")
        result["errors"].append(f"Prioritization failed: {str(e)}")
        priority = {
            "score": 50.0,
            "priority_level": "medium",
            "response_time": "24 hours",
            "reasoning": "Default priority (scoring failed)",
        }
        result["priority"] = priority

    # ── Step 3: Provider Assignment (optional) ─────────────────────────
    assignment = None
    if not skip_assignment:
        logger.info("Pipeline Step 3/3: Finding best provider...")
        try:
            complaint_for_assignment = {
                "category": final_category,
                "description": description,
                "location": location,
                "priority_level": priority.get("priority_level", "medium"),
                "user": user_info or {},
            }
            assignment = await find_best_provider(complaint_for_assignment)
            result["assignment"] = assignment
            logger.info(
                f"Assignment complete: provider={assignment.get('recommended_provider_name')}, "
                f"source={assignment.get('source')}"
            )
        except Exception as e:
            logger.error(f"Provider assignment failed: {e}")
            result["errors"].append(f"Assignment failed: {str(e)}")
    else:
        logger.info("Pipeline Step 3/3: Skipped (skip_assignment=True)")

    # ── Build enriched fields for complaint document ───────────────────
    result["enriched_fields"] = {
        "category": final_category,
        "subcategory": nlu.get("subcategory", ""),
        "priority_level": priority.get("priority_level", "medium"),
        "priority_score": priority.get("score", 50.0),
        "priority_reasoning": priority.get("reasoning", ""),
        "ai_analysis": {
            "category_confidence": 0.9 if nlu.get("source") == "sarvam_ai" else 0.7,
            "severity_words": nlu.get("urgency_keywords", []),
            "safety_risk": nlu.get("safety_risk", False),
            "detected_language": nlu.get("detected_language", "en"),
            "sentiment_score": nlu.get("sentiment_score", 0.5),
            "affected_scope": nlu.get("affected_scope", "single"),
            "key_issues": nlu.get("key_issues", []),
            "source": nlu.get("source", "unknown"),
        },
    }

    if assignment and assignment.get("recommended_provider_id"):
        result["enriched_fields"]["assigned_provider_id"] = assignment["recommended_provider_id"]
        result["enriched_fields"]["estimated_resolution_time"] = assignment.get("estimated_time")

    result["pipeline_status"] = "completed"
    error_count = len(result["errors"])
    if error_count > 0:
        result["pipeline_status"] = f"completed_with_{error_count}_errors"

    logger.info(f"Pipeline finished: status={result['pipeline_status']}")
    return result


async def analyze_for_chat(description: str) -> Dict[str, Any]:
    """
    Lightweight pipeline for chat — runs only NLU + Priority (no assignment).
    Used by the chat endpoint to provide real-time analysis feedback.

    Returns:
        Dict with detected_category, detected_priority, confidence, and full analysis.
    """
    result = await run_complaint_pipeline(
        description=description,
        skip_assignment=True,
    )

    nlu = result.get("nlu_analysis", {})
    priority = result.get("priority", {})

    return {
        "detected_category": nlu.get("category", "other"),
        "detected_subcategory": nlu.get("subcategory", ""),
        "detected_priority": priority.get("priority_level", "medium"),
        "priority_score": priority.get("score", 50.0),
        "confidence": 0.92 if nlu.get("source") == "sarvam_ai" else 0.75,
        "safety_risk": nlu.get("safety_risk", False),
        "urgency": nlu.get("urgency", "medium"),
        "sentiment_score": nlu.get("sentiment_score", 0.5),
        "detected_language": nlu.get("detected_language", "en"),
        "key_issues": nlu.get("key_issues", []),
        "source": nlu.get("source", "unknown"),
        "priority_reasoning": priority.get("reasoning", ""),
    }
