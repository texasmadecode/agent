"""
Celery configuration for background task processing.

This module sets up Celery for handling scheduled posts,
content generation, analytics processing, and other
background tasks.
"""

from celery import Celery
from celery.schedules import crontab
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create Celery instance
celery_app = Celery(
    "marketing_agent",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.content_tasks",
        "app.tasks.posting_tasks",
        "app.tasks.analytics_tasks",
        "app.tasks.report_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task routing
    task_routes={
        "app.tasks.posting_tasks.*": {"queue": "posting"},
        "app.tasks.content_tasks.*": {"queue": "content"},
        "app.tasks.analytics_tasks.*": {"queue": "analytics"},
        "app.tasks.report_tasks.*": {"queue": "reports"},
    },
    
    # Task serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    
    # Timezone
    timezone="UTC",
    enable_utc=True,
    
    # Task results
    result_expires=3600,  # 1 hour
    
    # Worker settings
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_max_tasks_per_child=50,
    
    # Retry settings
    task_retry_backoff=True,
    task_retry_backoff_max=700,
    task_retry_jitter=False,
)

# Periodic task schedule
celery_app.conf.beat_schedule = {
    # Check for scheduled posts every minute
    "check-scheduled-posts": {
        "task": "app.tasks.posting_tasks.check_scheduled_posts",
        "schedule": crontab(minute="*"),
    },
    
    # Generate daily analytics reports at 8 AM
    "daily-analytics-report": {
        "task": "app.tasks.report_tasks.generate_daily_report",
        "schedule": crontab(hour=8, minute=0),
    },
    
    # Generate weekly reports on Mondays at 9 AM
    "weekly-analytics-report": {
        "task": "app.tasks.report_tasks.generate_weekly_report",
        "schedule": crontab(hour=9, minute=0, day_of_week=1),
    },
    
    # Clean up old analytics data monthly
    "cleanup-old-analytics": {
        "task": "app.tasks.analytics_tasks.cleanup_old_data",
        "schedule": crontab(hour=2, minute=0, day_of_month=1),
    },
    
    # Update engagement metrics every 30 minutes
    "update-engagement-metrics": {
        "task": "app.tasks.analytics_tasks.update_engagement_metrics",
        "schedule": crontab(minute="*/30"),
    },
    
    # Check for failed posts and retry every hour
    "retry-failed-posts": {
        "task": "app.tasks.posting_tasks.retry_failed_posts",
        "schedule": crontab(minute=0),
    },
}


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery functionality."""
    print(f"Request: {self.request!r}")
    return "Debug task completed"


class CeleryManager:
    """Celery task management utilities."""
    
    @staticmethod
    def get_active_tasks():
        """Get list of active Celery tasks."""
        try:
            inspect = celery_app.control.inspect()
            active = inspect.active()
            return active
        except Exception as e:
            logger.error(f"Error getting active tasks: {e}")
            return {}
    
    @staticmethod
    def get_scheduled_tasks():
        """Get list of scheduled Celery tasks."""
        try:
            inspect = celery_app.control.inspect()
            scheduled = inspect.scheduled()
            return scheduled
        except Exception as e:
            logger.error(f"Error getting scheduled tasks: {e}")
            return {}
    
    @staticmethod
    def revoke_task(task_id: str, terminate: bool = False):
        """
        Revoke a Celery task.
        
        Args:
            task_id: The task ID to revoke
            terminate: Whether to terminate if task is running
        """
        try:
            celery_app.control.revoke(task_id, terminate=terminate)
            logger.info(f"Task {task_id} revoked successfully")
        except Exception as e:
            logger.error(f"Error revoking task {task_id}: {e}")
    
    @staticmethod
    def get_task_result(task_id: str):
        """
        Get the result of a Celery task.
        
        Args:
            task_id: The task ID
            
        Returns:
            Task result or None if not found
        """
        try:
            result = celery_app.AsyncResult(task_id)
            return {
                "id": task_id,
                "status": result.status,
                "result": result.result,
                "traceback": result.traceback
            }
        except Exception as e:
            logger.error(f"Error getting task result for {task_id}: {e}")
            return None


# Create global celery manager instance
celery_manager = CeleryManager()
