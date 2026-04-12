"""Input Understanding Agent using LangChain and Sarvam AI."""

from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
import logging

logger = logging.getLogger(__name__)


class ComplaintInput(BaseModel):
    """Structured complaint input extracted from user message."""

    category: str = Field(
        description="Problem category: electricity, water, sanitation, hvac, plumbing, maintenance, security, other"
    )
    subcategory: str = Field(description="Specific sub-category of the problem")
    location: str = Field(description="Exact location of the issue within the property")
    description: str = Field(description="Detailed description of the problem")
    severity_indicators: List[str] = Field(
        description="Key phrases from input indicating severity"
    )
    urgency_keywords: List[str] = Field(
        description="Words indicating time sensitivity"
    )
    affected_users: str = Field(
        description="Number of people affected: single, multiple, building"
    )
    safety_risk: bool = Field(description="Whether there's a safety hazard")
    media_analysis: Optional[str] = Field(
        description="Analysis of attached images/audio if any"
    )
    detected_language: str = Field(
        description="Language detected in user input (hi, en, ta, te, etc.)"
    )
    sentiment_score: float = Field(
        description="User frustration level 0-1, where 1 is most frustrated"
    )


# Priority indicators for the system prompt
PRIORITY_GUIDANCE = """
Consider these priority indicators:

SAFETY RISK (Automatic HIGH/CRITICAL):
- Electrical hazards: exposed wires, sparking, burning smell
- Gas leaks: gas smell, hissing sounds
- Fire risks: smoke, burning, overheating
- Structural damage: cracks, falling debris
- Water near electricity: flooding with electrical panels

BASIC NECESSITY (HIGH):
- No water supply
- No electricity (entire building)
- Blocked toilet (only one in unit)
- Sewage backup

COMFORT (MEDIUM):
- AC not working
- Minor water leaks
- Appliance malfunction
- Single room power outage

COSMETIC (LOW):
- Paint peeling
- Minor scratches
- General maintenance requests
"""

input_understanding_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are an intelligent complaint understanding agent for urban services.
Your task is to analyze user complaints and extract structured information.

You are powered by Sarvam AI, optimized for Indian languages and context.
Support these languages: Hindi (hi), English (en), Tamil (ta), Telugu (te),
Kannada (kn), Malayalam (ml), Bengali (bn), Marathi (mr), Gujarati (gu), Punjabi (pa).

{PRIORITY_GUIDANCE}

Extract entities, intent, and severity from the user's description.
Be accurate in category classification.
Detect the language correctly.

{{format_instructions}}
"""),
    ("human", "User complaint: {{user_input}}"),
    ("human", "Attached media context: {{media_context}}"),
])


def create_input_understanding_chain(llm):
    """
    Create the input understanding chain.

    Args:
        llm: LangChain LLM instance (Sarvam AI compatible)

    Returns:
        Runnable chain for processing complaints
    """
    parser = PydanticOutputParser(pydantic_object=ComplaintInput)

    chain = (
        RunnableParallel({
            "user_input": lambda x: x["user_input"],
            "media_context": lambda x: x.get("media_context", "No media attached"),
            "format_instructions": lambda x: parser.get_format_instructions(),
        })
        | input_understanding_prompt
        | llm
        | parser
    )

    return chain


async def analyze_image_async(image_data: bytes, llm=None) -> str:
    """
    Analyze complaint-related images.

    Args:
        image_data: Raw image bytes
        llm: Optional vision-capable LLM

    Returns:
        Description of what the image shows relevant to the complaint
    """
    # This would integrate with Sarvam AI vision API or another vision model
    # For now, return a placeholder that would be replaced with actual implementation

    logger.info("Analyzing image...")

    # TODO: Implement actual Sarvam AI vision integration
    # Example:
    # response = await sarvam_client.analyze_image(
    #     image=image_data,
    #     prompt="Describe any damage, leaks, or issues visible in this image related to home maintenance."
    # )
    # return response.analysis

    return "Image analysis pending - vision integration required"


async def transcribe_audio_async(audio_data: bytes) -> str:
    """
    Transcribe voice complaints using Sarvam AI speech-to-text.

    Args:
        audio_data: Raw audio bytes

    Returns:
        Transcribed text
    """
    logger.info("Transcribing audio...")

    # TODO: Implement Sarvam AI STT integration
    # Sarvam AI supports Indian language speech recognition

    # Example:
    # response = await sarvam_client.transcribe(
    #     audio=audio_data,
    #     language="hi"  # Auto-detect or specify
    # )
    # return response.text

    return "Audio transcription pending - STT integration required"


# Example usage
if __name__ == "__main__":
    # This would be used as follows:
    from langchain_community.llms import SarvamAI  # Placeholder import

    # llm = SarvamAI(api_key="your-key", model="sarvam-1")
    # chain = create_input_understanding_chain(llm)

    # result = chain.invoke({
    #     "user_input": "बिजली चली गई है और पूरा बिल्डिंग अंधेरे में है",
    #     "media_context": "No media"
    # })
    # print(result)
    pass
