import time
from celery import Celery


celery_app = Celery(broker='redis://127.0.0.1:6379/1', backend='redis://127.0.0.1:6379/2')


@celery_app.task()
def cpu_bound_function(a, b):
    a + b
    time.sleep(2)

    return 'Hello World'

