from celery import Celery
from src.ai.tasks_service import generate_summary
import asyncio

c_app = Celery()

c_app.config_from_object('src.config')

@c_app.task(
    bind=True,
    name="generate_summary",
    max_retries=3,
    default_retry_delay=10,
)
def generate_summary_task(self, user_uid: str, note_uid: str):
    try:
        return asyncio.run(
            generate_summary(user_uid, note_uid)
        )
    except ValueError:
        raise
    except Exception as exc:
        raise self.retry(exc=exc)



