"""
Base task classes for Celery tasks.

This module provides base task classes with common functionality
like database session handling.
"""

from celery import Task
import logging

from app.core.database import SessionLocal

logger = logging.getLogger(__name__)


class DatabaseTask(Task):
    """Base task class with database session handling."""
    
    def __call__(self, *args, **kwargs):
        """Execute task with database session."""
        with SessionLocal() as db:
            try:
                return self.run(*args, db=db, **kwargs)
            except Exception as e:
                db.rollback()
                logger.error(f"Task {self.name} failed: {e}")
                raise
            finally:
                db.close()