"""Custom LangChain LLM wrapper for Sarvam AI.

Sarvam AI exposes an OpenAI-compatible chat completions endpoint
at https://api.sarvam.ai/v1/chat/completions.
We use langchain's ChatOpenAI with a custom base_url to integrate it.
"""

import logging
from typing import Optional, List, Dict, Any
import httpx

from app.config import settings

logger = logging.getLogger(__name__)

# Available Sarvam AI models
SARVAM_MODELS = {
    "default": "sarvam-m",
    "small": "sarvam-m",
}


def get_sarvam_llm():
    """
    Create a Sarvam AI LLM instance using the OpenAI-compatible interface.
    Returns None if the API key is not configured.
    """
    if not settings.SARVAM_API_KEY:
        logger.warning("SARVAM_API_KEY not set — AI agents will use deterministic fallback")
        return None

    try:
        from langchain.chat_models import ChatOpenAI

        llm = ChatOpenAI(
            model=SARVAM_MODELS["default"],
            openai_api_key=settings.SARVAM_API_KEY,
            openai_api_base="https://api.sarvam.ai/v1",
            temperature=0.1,
            max_tokens=1024,
        )
        logger.info("Sarvam AI LLM initialized successfully")
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize Sarvam AI LLM: {e}")
        return None


async def sarvam_chat(
    messages: List[Dict[str, str]],
    model: str = "sarvam-m",
    temperature: float = 0.1,
    max_tokens: int = 1024,
) -> Optional[str]:
    """
    Direct async call to Sarvam AI chat completions API.
    Falls back to None if call fails.
    """
    if not settings.SARVAM_API_KEY:
        return None

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.sarvam.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.SARVAM_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]

            # Strip <think>...</think> tags if present (Sarvam reasoning mode)
            if "<think>" in content:
                import re
                content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

            return content

    except Exception as e:
        logger.error(f"Sarvam AI API call failed: {e}")
        return None
