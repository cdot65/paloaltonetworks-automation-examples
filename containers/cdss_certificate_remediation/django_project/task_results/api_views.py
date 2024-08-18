from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TaskResult
from .serializers import TaskResultSerializer
import logging

logger = logging.getLogger(__name__)


class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "task_id"]
    search_fields = ["task_id", "status", "result"]
    ordering_fields = ["created_at", "task_id", "status"]

    def list(self, request, *args, **kwargs):
        logger.info(f"Request query params: {request.query_params}")
        queryset = self.filter_queryset(self.get_queryset())
        logger.info(f"Filtered queryset count: {queryset.count()}")
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
            logger.info(f"Filter backend: {backend.__name__}")
            logger.info(f"Filtered queryset: {queryset.query}")
        return queryset

    @action(detail=True, methods=["get"])
    def preferred_connection(self, request, pk=None):
        inventory = self.get_object()
        return Response(
            {"preferred_connection_address": inventory.get_connection_address()}
        )
