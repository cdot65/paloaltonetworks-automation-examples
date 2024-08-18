# django_project/task_results/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/task_status/", consumers.TaskStatusConsumer.as_asgi()),
]
