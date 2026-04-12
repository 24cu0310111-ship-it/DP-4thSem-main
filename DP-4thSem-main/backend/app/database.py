"""MongoDB connection and collection management."""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Global MongoDB client and database references
client: Optional[AsyncIOMotorClient] = None
db = None


async def connect_db():
    """Connect to MongoDB on application startup."""
    global client, db
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        # Verify connection
        await client.admin.command("ping")
        logger.info(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")

        # Create indexes
        await create_indexes()
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_db():
    """Close MongoDB connection on application shutdown."""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")


async def create_indexes():
    """Create database indexes for performance."""
    # Users collection
    await db.users.create_index("phone", unique=True)
    await db.users.create_index("email", unique=True, sparse=True)
    await db.users.create_index("role")

    # Complaints collection
    await db.complaints.create_index("complaint_id", unique=True)
    await db.complaints.create_index("user_id")
    await db.complaints.create_index("status")
    await db.complaints.create_index("priority_level")
    await db.complaints.create_index("category")
    await db.complaints.create_index([("created_at", -1)])

    # Service providers collection
    await db.service_providers.create_index("platform")
    await db.service_providers.create_index("availability_status")
    await db.service_providers.create_index("service_types")
    await db.service_providers.create_index("service_areas")

    # Timeline collection
    await db.complaint_timeline.create_index("complaint_id")
    await db.complaint_timeline.create_index([("created_at", 1)])

    # Admin notes
    await db.admin_notes.create_index("complaint_id")

    # Audit logs
    await db.audit_logs.create_index("user_id")
    await db.audit_logs.create_index([("created_at", -1)])

    logger.info("Database indexes created")


def get_db():
    """Get database instance."""
    return db


# Collection accessors
def users_collection():
    return db.users


def complaints_collection():
    return db.complaints


def providers_collection():
    return db.service_providers


def timeline_collection():
    return db.complaint_timeline


def notes_collection():
    return db.admin_notes


def audit_collection():
    return db.audit_logs


def chat_collection():
    return db.chat_history
