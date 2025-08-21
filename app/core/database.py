"""
Database configuration and session management.

This module sets up SQLAlchemy with PostgreSQL and provides
database session management for the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging

from app.core.config import get_database_url

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    get_database_url(),
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


class DatabaseManager:
    """Database management utilities."""
    
    @staticmethod
    def create_tables():
        """Create all database tables."""
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    @staticmethod
    def drop_tables():
        """Drop all database tables."""
        try:
            Base.metadata.drop_all(bind=engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Error dropping database tables: {e}")
            raise
    
    @staticmethod
    def get_session() -> Session:
        """Get a new database session."""
        return SessionLocal()


# Initialize database manager
db_manager = DatabaseManager()
