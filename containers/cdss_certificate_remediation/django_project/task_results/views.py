from rest_framework import viewsets
from .models import TaskResult
from .serializers import TaskResultSerializer


class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    filterset_fields = ["status", "task_id"]
    search_fields = ["task_id", "status"]
    ordering_fields = ["created_at", "updated_at"]
