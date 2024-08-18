# django_project/inventory/api_views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TaskResult
from .serializers import TaskResultSerializer


class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "task_id",
        "status",
        "result",
    ]
    ordering_fields = [
        "created_at",
        "task_id",
        "status",
        "result",
    ]

    @action(detail=True, methods=["get"])
    def preferred_connection(self, request, pk=None):
        inventory = self.get_object()
        return Response(
            {"preferred_connection_address": inventory.get_connection_address()}
        )
