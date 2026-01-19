from celery import Celery
from app.core.config import settings
import time

celery_app = Celery(
    'tasks',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    include=["app.tasks.tasks"]
)