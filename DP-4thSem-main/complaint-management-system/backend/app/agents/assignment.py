"""Assignment Agent for matching complaints to service providers."""

from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableParallel
import logging

logger = logging.getLogger(__name__)


class ServiceProvider(BaseModel):
    """Service provider from external platform."""

    platform: str = Field(
        description="Platform name: urban_company, taskrabbit, handy, local"
    )
    provider_name: str = Field(description="Name of the service provider/business")
    service_type: str = Field(description="Primary service type")
    rating: float = Field(description="Provider rating 0-5")
    reviews_count: int = Field(description="Number of reviews")
    price_range: str = Field(description="Price range: $, $$, $$$")
    estimated_price: Optional[float] = Field(description="Estimated price in local currency")
    availability: str = Field(
        description="Availability status: Available, Next Day, 2-3 days"
    )
    distance_km: float = Field(description="Distance from complaint location in km")
    platform_icon: str = Field(description="URL or identifier for platform logo")
    deep_link: str = Field(description="Direct booking URL for this provider")


class AssignmentRecommendation(BaseModel):
    """Recommended service providers for a complaint."""

    complaint_id: str
    category: str
    location: str
    recommended_providers: List[ServiceProvider] = Field(
        description="List of top recommended providers"
    )
    best_match_reason: str = Field(
        description="Explanation for why the top provider is the best match"
    )
    filters_applied: dict = Field(
        description="Filters that were applied in selection"
    )


# Platform configurations
PLATFORM_CONFIG = {
    "urban_company": {
        "display_name": "Urban Company",
        "icon": "UC",
        "color": "#0066FF",
        "services": ["plumbing", "electrical", "appliance_repair", "cleaning", "maintenance"],
        "booking_url_template": "https://urbancompany.com/book?provider={provider_id}",
    },
    "taskrabbit": {
        "display_name": "TaskRabbit",
        "icon": "TR",
        "color": "#EF4444",
        "services": ["handyman", "mounting", "assembly", "minor_repairs", "furniture"],
        "booking_url_template": "https://taskrabbit.com/taskers/{provider_id}",
    },
    "handy": {
        "display_name": "Handy",
        "icon": "H",
        "color": "#10B981",
        "services": ["cleaning", "home_services", "maintenance", "repairs"],
        "booking_url_template": "https://handy.com/book/{provider_id}",
    },
    "local": {
        "display_name": "Local Provider",
        "icon": "🏪",
        "color": "#6B7280",
        "services": ["all"],
        "booking_url_template": "tel:{phone}",
    },
}

assignment_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a service provider matching agent for urban services.
Your task is to recommend suitable service providers based on complaint details.

AVAILABLE PLATFORMS:
1. Urban Company - Professional home services (plumbing, electrical, appliances)
2. TaskRabbit - Task-based services (handyman, mounting, assembly)
3. Handy - Cleaning and home maintenance services
4. Local Providers - Area-specific independent contractors

MATCHING CRITERIA:
1. Service Type Match - Provider must offer the required service category
2. Location Coverage - Provider must serve the complaint area
3. Availability - Prefer providers available within the required timeframe
4. Rating - Higher rated providers preferred (minimum 4.0)
5. Price - Consider user's likely budget based on problem severity

SELECTION LOGIC:
- For electrical/plumbing emergencies → Prioritize availability and proximity
- For routine maintenance → Prioritize rating and price
- For specialized work → Prioritize provider expertise and reviews

Return top 5 providers sorted by overall match score.
Include clear reasoning for the best match recommendation.

{format_instructions}
"""),
    ("human", """
Complaint Details:
- Complaint ID: {complaint_id}
- Category: {category}
- Subcategory: {subcategory}
- Location: {location}
- Priority Level: {priority_level}
- Required Response Time: {response_time}

Available Providers in Database:
{available_providers}
"""),
])


def create_assignment_chain(llm):
    """
    Create the assignment recommendation chain.

    Args:
        llm: LangChain LLM instance

    Returns:
        Runnable chain for provider matching
    """
    parser = PydanticOutputParser(pydantic_object=AssignmentRecommendation)

    chain = (
        assignment_prompt
        | llm
        | parser
    )

    return chain


def filter_providers_by_category(
    providers: list,
    category: str,
    subcategory: Optional[str] = None,
) -> list:
    """
    Filter providers by service category.

    Args:
        providers: List of provider dictionaries
        category: Primary category
        subcategory: Optional subcategory

    Returns:
        Filtered list of providers
    """
    # Map complaint categories to provider service types
    category_mapping = {
        "electricity": ["electrical", "electrician"],
        "water": ["plumbing", "water_heater"],
        "plumbing": ["plumbing", "pipe_repair", "leak"],
        "sanitation": ["cleaning", "sanitation", "drain_cleaning"],
        "hvac": ["hvac", "ac_repair", "heating"],
        "maintenance": ["maintenance", "handyman", "repairs"],
        "security": ["security", "locksmith"],
    }

    relevant_services = category_mapping.get(category.lower(), [])

    filtered = []
    for provider in providers:
        provider_services = [s.lower() for s in provider.get("service_types", [])]
        if any(service in provider_services for service in relevant_services):
            filtered.append(provider)

    return filtered


def filter_providers_by_location(
    providers: list,
    pincode: str,
) -> list:
    """
    Filter providers by service area (pincode).

    Args:
        providers: List of provider dictionaries
        pincode: Area pincode

    Returns:
        Filtered list of providers
    """
    filtered = []
    for provider in providers:
        service_areas = provider.get("service_areas", [])
        if pincode in service_areas:
            filtered.append(provider)

    return filtered


def rank_providers(
    providers: list,
    priority_level: str,
) -> list:
    """
    Rank providers by relevance score.

    Args:
        providers: List of provider dictionaries
        priority_level: Complaint priority level

    Returns:
        Sorted list by match score
    """
    def calculate_match_score(provider: dict) -> float:
        score = 0.0

        # Rating score (max 40 points)
        rating = provider.get("rating", 0)
        score += rating * 8  # 5 * 8 = 40

        # Reviews count score (max 20 points)
        reviews = provider.get("reviews_count", 0)
        if reviews >= 100:
            score += 20
        elif reviews >= 50:
            score += 15
        elif reviews >= 20:
            score += 10
        elif reviews > 0:
            score += 5

        # Availability score (max 30 points)
        availability = provider.get("availability_status", "unavailable")
        if priority_level in ["critical", "high"]:
            # Urgent: prioritize immediate availability
            if availability == "available":
                score += 30
            elif availability == "busy":
                score += 10
        else:
            # Non-urgent: any availability is fine
            if availability == "available":
                score += 30
            elif availability == "busy":
                score += 20
            else:
                score += 5

        # Price score (max 10 points) - prefer moderate pricing
        price_range = provider.get("price_range", "$$")
        if price_range == "$$":
            score += 10
        elif price_range == "$":
            score += 8
        elif price_range == "$$$":
            score += 5

        return score

    return sorted(providers, key=calculate_match_score, reverse=True)


def generate_deep_link(
    platform: str,
    provider_id: str,
    phone: Optional[str] = None,
) -> str:
    """
    Generate booking deep link for a provider.

    Args:
        platform: Platform identifier
        provider_id: Provider's ID on the platform
        phone: Phone number for local providers

    Returns:
        Deep link URL
    """
    config = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG["local"])
    template = config["booking_url_template"]

    if platform == "local" and phone:
        return template.format(phone=phone)

    return template.format(provider_id=provider_id)


# Example usage
if __name__ == "__main__":
    # Sample providers from database
    sample_providers = [
        {
            "id": "prov-001",
            "name": "ABC Plumbing Services",
            "platform": "urban_company",
            "service_types": ["plumbing", "water_heater", "drain_cleaning"],
            "rating": 4.8,
            "reviews_count": 234,
            "price_range": "$$",
            "service_areas": ["122001", "122002"],
            "availability_status": "available",
        },
        {
            "id": "prov-002",
            "name": "QuickFix Electricians",
            "platform": "urban_company",
            "service_types": ["electrical", "wiring", "appliance_repair"],
            "rating": 4.6,
            "reviews_count": 189,
            "price_range": "$$",
            "service_areas": ["122001", "122003"],
            "availability_status": "busy",
        },
    ]

    # Filter and rank
    filtered = filter_providers_by_category(sample_providers, "plumbing")
    ranked = rank_providers(filtered, "high")

    print(f"Top provider: {ranked[0]['name']}") if ranked else print("No providers found")
