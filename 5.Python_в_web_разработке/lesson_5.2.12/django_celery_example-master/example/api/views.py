from rest_framework.response import Response
from rest_framework.views import APIView

from example.tasks import cpu_bound
from django_celery_example.celery import get_result


class TaskViewGet(APIView):

    def get(self, request, *args, **kwargs):
        task_id = kwargs['task_id']
        task_result = get_result(task_id)
        return Response({'status': task_result.status, 'result': task_result.result})


class TaskViewCreate(APIView):

    def post(self, request, *args, **kwargs):
        task = cpu_bound.delay()
        return Response({'task_id': task.id})
