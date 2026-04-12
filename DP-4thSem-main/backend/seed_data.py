"""Seed MongoDB with demo data matching the frontend mock data."""

import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MONGODB_URL = "mongodb://localhost:27017"
MONGODB_DB_NAME = "scms"


async def seed():
    """Seed the database with demo data."""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB_NAME]

    print("🌱 Seeding SCMS database...")

    # --- Clear existing data ---
    await db.users.delete_many({})
    await db.complaints.delete_many({})
    await db.service_providers.delete_many({})
    await db.complaint_timeline.delete_many({})
    await db.admin_notes.delete_many({})
    print("  ✓ Cleared existing data")

    # --- Users ---
    users = [
        {
            "_id": "550e8400-e29b-41d4-a716-446655440000",
            "phone": "+919876543210",
            "email": "sarah.chen@example.com",
            "name": "Sarah Chen",
            "password_hash": pwd_context.hash("user123"),
            "role": "user",
            "address": {
                "flat_no": "A-101",
                "building": "Skyview Towers",
                "area": "Sector 15",
                "city": "Gurgaon",
                "pincode": "122001",
            },
            "is_active": True,
            "created_at": datetime(2024, 1, 15, 10, 30),
            "updated_at": datetime(2024, 1, 15, 10, 30),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440099",
            "phone": "+919876543299",
            "email": "admin@scms.com",
            "name": "Marcus Thorne",
            "password_hash": pwd_context.hash("admin123"),
            "role": "admin",
            "address": {
                "flat_no": "Office",
                "building": "SCMS HQ",
                "area": "Sector 1",
                "city": "Gurgaon",
                "pincode": "122001",
            },
            "is_active": True,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440010",
            "phone": "+919876543211",
            "email": "raj.patel@example.com",
            "name": "Raj Patel",
            "password_hash": pwd_context.hash("user123"),
            "role": "user",
            "address": {
                "flat_no": "B-204",
                "building": "Skyview Towers",
                "area": "Sector 15",
                "city": "Gurgaon",
                "pincode": "122001",
            },
            "is_active": True,
            "created_at": datetime(2024, 1, 10),
            "updated_at": datetime(2024, 1, 10),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440011",
            "phone": "+919876543212",
            "email": "elena.rodriguez@example.com",
            "name": "Elena Rodriguez",
            "password_hash": pwd_context.hash("user123"),
            "role": "user",
            "address": {
                "flat_no": "C-302",
                "building": "Central Mall",
                "area": "Sector 20",
                "city": "Gurgaon",
                "pincode": "122002",
            },
            "is_active": True,
            "created_at": datetime(2024, 1, 12),
            "updated_at": datetime(2024, 1, 12),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440012",
            "phone": "+919876543213",
            "email": "amit.sharma@example.com",
            "name": "Amit Sharma",
            "password_hash": pwd_context.hash("user123"),
            "role": "user",
            "address": {
                "flat_no": "D-501",
                "building": "Elite Estates",
                "area": "Sector 10",
                "city": "Gurgaon",
                "pincode": "122001",
            },
            "is_active": True,
            "created_at": datetime(2024, 1, 8),
            "updated_at": datetime(2024, 1, 8),
        },
    ]
    await db.users.insert_many(users)
    print(f"  ✓ Inserted {len(users)} users")

    # --- Complaints (match frontend mock data exactly) ---
    sarah_address = {"flat_no": "A-101", "building": "Skyview Towers", "area": "Sector 15", "city": "Gurgaon", "pincode": "122001"}

    complaints = [
        {
            "_id": "550e8400-e29b-41d4-a716-446655440001",
            "complaint_id": "CM-20240115-0001",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "user": {"name": "Sarah Chen", "phone": "+919876543210", "address": sarah_address},
            "category": "plumbing",
            "subcategory": "pipe_leak",
            "description": "Water pipe leaking in kitchen, water spreading across the floor rapidly.",
            "location": "Kitchen sink area",
            "priority_level": "critical",
            "priority_score": 92.5,
            "priority_reasoning": "Active water leak with flooding risk, affects daily living and may cause property damage.",
            "status": "in_progress",
            "ai_analysis": {
                "category_confidence": 0.95,
                "severity_words": ["flooding", "rapidly"],
                "safety_risk": False,
                "detected_language": "en",
                "sentiment_score": 0.78,
            },
            "media_urls": [],
            "assigned_provider_id": None,
            "estimated_resolution_time": "2024-01-15T18:00:00Z",
            "created_at": datetime(2024, 1, 15, 11, 0),
            "updated_at": datetime(2024, 1, 15, 14, 30),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440002",
            "complaint_id": "CM-20240115-0002",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "user": {"name": "Sarah Chen", "phone": "+919876543210", "address": sarah_address},
            "category": "electricity",
            "subcategory": "power_outage",
            "description": "Complete power outage in flat since morning. No electricity in any room.",
            "location": "Entire flat A-101",
            "priority_level": "high",
            "priority_score": 78.5,
            "priority_reasoning": "Complete power loss affecting all appliances and lighting.",
            "status": "open",
            "media_urls": [],
            "created_at": datetime(2024, 1, 16, 8, 0),
            "updated_at": datetime(2024, 1, 16, 8, 0),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440003",
            "complaint_id": "CM-20240114-0003",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "user": {"name": "Sarah Chen", "phone": "+919876543210", "address": sarah_address},
            "category": "maintenance",
            "subcategory": "paint_peeling",
            "description": "Paint peeling off the bathroom ceiling due to moisture.",
            "location": "Master bathroom ceiling",
            "priority_level": "low",
            "priority_score": 25.0,
            "priority_reasoning": "Cosmetic issue, no immediate safety or functional impact.",
            "status": "resolved",
            "media_urls": [],
            "actual_resolution_time": "2024-01-15T16:00:00Z",
            "user_satisfaction": 4,
            "created_at": datetime(2024, 1, 14, 9, 0),
            "updated_at": datetime(2024, 1, 15, 16, 0),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440004",
            "complaint_id": "CM-20240116-0004",
            "user_id": "550e8400-e29b-41d4-a716-446655440010",
            "user": {"name": "Raj Patel", "phone": "+919876543211", "address": {"flat_no": "B-204", "building": "Skyview Towers", "area": "Sector 15", "city": "Gurgaon", "pincode": "122001"}},
            "category": "water",
            "subcategory": "low_pressure",
            "description": "Very low water pressure on 2nd floor since yesterday.",
            "location": "Floor 2, all units",
            "priority_level": "medium",
            "priority_score": 55.0,
            "priority_reasoning": "Affects multiple residents on the same floor.",
            "status": "assigned",
            "media_urls": [],
            "created_at": datetime(2024, 1, 16, 6, 30),
            "updated_at": datetime(2024, 1, 16, 10, 0),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440005",
            "complaint_id": "CM-20240116-0005",
            "user_id": "550e8400-e29b-41d4-a716-446655440011",
            "user": {"name": "Elena Rodriguez", "phone": "+919876543212", "address": {"flat_no": "C-302", "building": "Central Mall", "area": "Sector 20", "city": "Gurgaon", "pincode": "122002"}},
            "category": "hvac",
            "subcategory": "ac_malfunction",
            "description": "Central AC not cooling in the food court area. Temperature rising.",
            "location": "Food Court, Level 3",
            "priority_level": "high",
            "priority_score": 82.0,
            "priority_reasoning": "Affects commercial space with high foot traffic, potential health concern.",
            "status": "open",
            "media_urls": [],
            "created_at": datetime(2024, 1, 16, 12, 0),
            "updated_at": datetime(2024, 1, 16, 12, 0),
        },
        {
            "_id": "550e8400-e29b-41d4-a716-446655440006",
            "complaint_id": "CM-20240116-0006",
            "user_id": "550e8400-e29b-41d4-a716-446655440012",
            "user": {"name": "Amit Sharma", "phone": "+919876543213", "address": {"flat_no": "D-501", "building": "Elite Estates", "area": "Sector 10", "city": "Gurgaon", "pincode": "122001"}},
            "category": "security",
            "subcategory": "broken_lock",
            "description": "Main entrance gate lock is broken. Security compromised.",
            "location": "Main entrance gate",
            "priority_level": "critical",
            "priority_score": 95.0,
            "priority_reasoning": "Security breach risk, affects all residents.",
            "status": "in_progress",
            "media_urls": [],
            "created_at": datetime(2024, 1, 16, 7, 0),
            "updated_at": datetime(2024, 1, 16, 8, 30),
        },
    ]
    await db.complaints.insert_many(complaints)
    print(f"  ✓ Inserted {len(complaints)} complaints")

    # --- Service Providers ---
    providers = [
        {
            "_id": "prov-quickfix-001",
            "platform": "urban_company",
            "platform_provider_id": "UC-QF-001",
            "name": "QuickFix Plumbing",
            "service_types": ["plumbing", "pipe_repair", "leak", "drain_cleaning", "water_heater"],
            "rating": 4.8,
            "reviews_count": 234,
            "price_range": "$$",
            "service_areas": ["122001", "122002", "Sector 15", "Sector 20"],
            "availability_status": "available",
            "avg_response_time": 45,
            "deep_link_template": "https://urbancompany.com/book?provider=UC-QF-001",
            "is_active": True,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1),
        },
        {
            "_id": "prov-pipeworks-002",
            "platform": "urban_company",
            "platform_provider_id": "UC-PW-002",
            "name": "PipeWorks Pro",
            "service_types": ["plumbing", "pipe_repair", "water_heater", "drain_cleaning"],
            "rating": 4.7,
            "reviews_count": 198,
            "price_range": "$$$",
            "service_areas": ["122001", "122003", "Sector 15", "Sector 10"],
            "availability_status": "available",
            "avg_response_time": 35,
            "deep_link_template": "https://urbancompany.com/book?provider=UC-PW-002",
            "is_active": True,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1),
        },
        {
            "_id": "prov-handyman-003",
            "platform": "taskrabbit",
            "platform_provider_id": "TR-HH-003",
            "name": "HandyMan Heroes",
            "service_types": ["plumbing", "electrical", "maintenance", "handyman", "repairs", "general"],
            "rating": 4.3,
            "reviews_count": 156,
            "price_range": "$",
            "service_areas": ["122001", "122002", "122003", "Sector 15", "Sector 20", "Sector 10"],
            "availability_status": "available",
            "avg_response_time": 60,
            "deep_link_template": "https://taskrabbit.com/taskers/TR-HH-003",
            "is_active": True,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1),
        },
        {
            "_id": "prov-sparkelectric-004",
            "platform": "urban_company",
            "platform_provider_id": "UC-SE-004",
            "name": "SparkElectric Solutions",
            "service_types": ["electrical", "electrician", "wiring", "appliance_repair"],
            "rating": 4.9,
            "reviews_count": 312,
            "price_range": "$$",
            "service_areas": ["122001", "122002", "Sector 15"],
            "availability_status": "available",
            "avg_response_time": 30,
            "deep_link_template": "https://urbancompany.com/book?provider=UC-SE-004",
            "is_active": True,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1),
        },
        {
            "_id": "prov-coolbreeze-005",
            "platform": "handy",
            "platform_provider_id": "H-CB-005",
            "name": "CoolBreeze HVAC",
            "service_types": ["hvac", "ac_repair", "heating", "cooling"],
            "rating": 4.5,
            "reviews_count": 89,
            "price_range": "$$$",
            "service_areas": ["122001", "122002", "122003", "Sector 15", "Sector 20"],
            "availability_status": "available",
            "avg_response_time": 50,
            "deep_link_template": "https://handy.com/book/H-CB-005",
            "is_active": True,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1),
        },
        {
            "_id": "prov-securelock-006",
            "platform": "local",
            "platform_provider_id": "LCL-SL-006",
            "name": "SecureLock Masters",
            "service_types": ["security", "locksmith", "cctv"],
            "rating": 4.6,
            "reviews_count": 67,
            "price_range": "$$",
            "service_areas": ["122001", "Sector 10", "Sector 15"],
            "availability_status": "available",
            "avg_response_time": 40,
            "deep_link_template": "tel:+919876599999",
            "is_active": True,
            "created_at": datetime(2024, 1, 1),
            "updated_at": datetime(2024, 1, 1),
        },
    ]
    await db.service_providers.insert_many(providers)
    print(f"  ✓ Inserted {len(providers)} service providers")

    # --- Timeline events for first complaint ---
    timeline = [
        {
            "_id": "tl-001",
            "complaint_id": "CM-20240115-0001",
            "event_type": "created",
            "event_data": {},
            "performed_by": None,
            "performed_by_name": None,
            "created_at": datetime(2024, 1, 15, 11, 0),
        },
        {
            "_id": "tl-002",
            "complaint_id": "CM-20240115-0001",
            "event_type": "prioritized",
            "event_data": {
                "priority_level": "critical",
                "priority_score": 92.5,
                "reasoning": "Active water leak with flooding risk",
            },
            "performed_by": None,
            "performed_by_name": None,
            "created_at": datetime(2024, 1, 15, 11, 0, 5),
        },
        {
            "_id": "tl-003",
            "complaint_id": "CM-20240115-0001",
            "event_type": "assigned",
            "event_data": {
                "provider_name": "QuickFix Plumbing",
                "platform": "urban_company",
            },
            "performed_by": "550e8400-e29b-41d4-a716-446655440099",
            "performed_by_name": "Marcus Thorne",
            "created_at": datetime(2024, 1, 15, 12, 30),
        },
        {
            "_id": "tl-004",
            "complaint_id": "CM-20240115-0001",
            "event_type": "status_changed",
            "event_data": {
                "previous_status": "open",
                "new_status": "in_progress",
            },
            "performed_by": "550e8400-e29b-41d4-a716-446655440099",
            "performed_by_name": "Marcus Thorne",
            "created_at": datetime(2024, 1, 15, 14, 30),
        },
    ]
    await db.complaint_timeline.insert_many(timeline)
    print(f"  ✓ Inserted {len(timeline)} timeline events")

    # --- Create indexes ---
    await db.users.create_index("phone", unique=True)
    await db.users.create_index("email", unique=True, sparse=True)
    await db.users.create_index("role")
    await db.complaints.create_index("complaint_id", unique=True)
    await db.complaints.create_index("user_id")
    await db.complaints.create_index("status")
    await db.complaints.create_index("priority_level")
    await db.complaints.create_index("category")
    await db.service_providers.create_index("platform")
    await db.complaint_timeline.create_index("complaint_id")
    print("  ✓ Created indexes")

    print("\n✅ Database seeded successfully!")
    print("\n📋 Demo Credentials:")
    print("  User:  phone=+919876543210  password=user123")
    print("  Admin: phone=admin          password=admin123")

    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
