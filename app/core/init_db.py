"""
Database initialization and sample data creation.

This module provides functions to initialize the database
with sample data for development and testing.
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base, User, Client, SocialAccount, Campaign, ContentItem, ContentType
from app.core.security import SecurityManager
import logging

logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize database with sample data."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("Adding sample data...")
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).first():
            logger.info("Database already initialized")
            return
        
        # Create sample user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=SecurityManager.get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # Create sample client
        sample_client = Client(
            name="Sample Company",
            description="A sample client for testing",
            website="https://example.com",
            user_id=admin_user.id
        )
        db.add(sample_client)
        db.commit()
        db.refresh(sample_client)
        
        # Create sample social account
        social_account = SocialAccount(
            platform="instagram",
            account_name="@samplecompany",
            access_token="sample_token",  # In real app, this would be encrypted
            account_id="123456789",
            client_id=sample_client.id
        )
        db.add(social_account)
        db.commit()
        
        # Create sample campaign
        campaign = Campaign(
            name="Sample Marketing Campaign",
            description="A test campaign for demonstration",
            start_date=None,
            end_date=None,
            budget="$1000",
            target_audience={"demographics": "Tech enthusiasts", "age_range": "25-45"},
            client_id=sample_client.id
        )
        db.add(campaign)
        db.commit()
        
        # Create sample content
        content = ContentItem(
            title="Welcome Post",
            content_data="Welcome to our automated marketing platform!",
            content_type="text",
            tags=["marketing", "automation", "tech"],
            campaign_id=campaign.id,
            client_id=sample_client.id
        )
        db.add(content)
        db.commit()
        
        logger.info("Sample data created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
