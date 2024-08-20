# django_project/inventory/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/jobs/", consumers.JobsConsumer.as_asgi()),
]
