from src.celery_task import c_app


@c_app.task
def add_numbers(a: int, b: int) -> int:
    return a + b