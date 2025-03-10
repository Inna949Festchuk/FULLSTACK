
from django.urls import path, include
from example.api.views import TaskViewGet, TaskViewCreate
from rest_framework import routers

app_name = 'example'



urlpatterns = [
    path('task/<task_id>', TaskViewGet.as_view()),
    path('task', TaskViewCreate.as_view()),
]