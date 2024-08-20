# django_project/jobs/views.py

import logging
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Job
from .serializers import JobSerializer

logger = logging.getLogger(__name__)


class JobViewSet(viewsets.ReadOnlyModelViewSet):
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
    ]
    ordering_fields = [
        "created_at",
        "updated_at",
    ]

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
