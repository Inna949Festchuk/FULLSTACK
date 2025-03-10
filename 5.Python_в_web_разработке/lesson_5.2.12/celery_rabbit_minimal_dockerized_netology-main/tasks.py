import os
import time

from celery import Celery

BACKEND = os.getenv("BACKEND")
BROKER = os.getenv("BROKER")

celery_app = Celery(
    broker=BROKER,
    backend=BACKEND,
    broker_connection_retry_on_startup=True,
)


@celery_app.task()
def cpu_bound_function(a, b):
    a + b
    time.sleep(2)

    return a + b
