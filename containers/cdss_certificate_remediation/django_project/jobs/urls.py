# django_project/jobs/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobListView, JobDeleteView, JobDetailView, AutomationCreateView

app_name = "jobs"

urlpatterns = [
    path(
        "",
        JobListView.as_view(),
        name="job_list",
    ),
    path(
        "<int:pk>/",
        JobDetailView.as_view(),
        name="job_detail",
    ),
    path(
        "create/",
        AutomationCreateView.as_view(),
        name="automation_create",
    ),
    path(
        "<int:pk>/delete/",
        JobDeleteView.as_view(),
        name="job_delete",
    ),
]
