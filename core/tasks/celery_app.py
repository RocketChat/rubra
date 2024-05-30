import redis
from celery import Celery
from typing import cast
import core.config as configs


redis_client = cast(redis.Redis, redis.Redis.from_url(configs.redis_url)) # annoyingly from_url returns None, not Self
app = Celery("tasks", broker=configs.redis_url)

app.autodiscover_tasks(["core.tasks"])  # Explicitly discover tasks in 'app' package
