from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskResultViewSet

router = DefaultRouter()
router.register(r"task-results", TaskResultViewSet)

app_name = "task_results"

urlpatterns = [
    path("", include(router.urls)),
]
