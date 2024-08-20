# django_project/jobs/api_views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
import logging

logger = logging.getLogger(__name__)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "status",
        "job_id",
    ]
    search_fields = [
        "job_id",
        "status",
        "result",
    ]
    ordering_fields = [
        "created_at",
        "job_id",
        "status",
    ]

    def list(self, request, *args, **kwargs):
        # logger.info(f"Request query params: {request.query_params}")
        queryset = self.filter_queryset(self.get_queryset())
        logger.info(f"Filtered queryset count: {queryset.count()}")
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
            # logger.info(f"Filter backend: {backend.__name__}")
            # logger.info(f"Filtered queryset: {queryset.query}")
        return queryset

    @action(detail=True, methods=["get"])
    def preferred_connection(self, request, pk=None):
        inventory = self.get_object()
        return Response(
            {"preferred_connection_address": inventory.get_connection_address()}
        )
