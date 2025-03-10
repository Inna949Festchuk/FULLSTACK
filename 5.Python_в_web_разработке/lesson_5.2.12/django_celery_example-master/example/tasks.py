import time
import random
from celery import shared_task


@shared_task
def cpu_bound():
    time.sleep(10)
    return random.randint(1, 100)