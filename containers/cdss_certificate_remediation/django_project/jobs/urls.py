# django_project/jobs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet

router = DefaultRouter()
router.register(r"jobs", JobViewSet)

app_name = "jobs"

urlpatterns = [
    path("", include(router.urls)),
]
