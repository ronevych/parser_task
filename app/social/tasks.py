from celery import shared_task
from celery.utils.log import get_task_logger
from social.services import fetch_users, fetch_posts, fetch_comments

logger = get_task_logger(__name__)

@shared_task
def sync_users_task():
    """
    Background task for users sync.
    """
    logger.info("Task sync_users_task started.")
    fetch_users()
    logger.info("Task sync_users_task finished.")

@shared_task
def sync_posts_task():
    """
    Background task for post sync.
    """
    logger.info("Task sync_posts_task started.")
    fetch_posts()
    logger.info("Task sync_posts_task finished.")

@shared_task
def sync_comments_task():
    """
    Фонова задача для коментарів.
    """
    logger.info("Task sync_comments_task started.")
    fetch_comments()
    logger.info("Task sync_comments_task finished.")

@shared_task
def sync_full_flow_task():
    """
    Full flow chain. Users first, then posts, so we don't damage data.
    """
    logger.info("Starting full sync flow...")
    fetch_users()
    fetch_posts()
    fetch_comments()
    logger.info("Full sync flow finished.")