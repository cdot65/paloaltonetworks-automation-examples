# cdss_certificate_remediation/inventory/api_views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Inventory
from .serializers import InventorySerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "device_type",
        "hostname",
        "username",
        "connection_hostname",
        "connection_ipv4",
        "connection_ipv6",
    ]
    ordering_fields = ["device_type", "hostname", "username"]

    @action(detail=True, methods=["get"])
    def preferred_connection(self, request, pk=None):
        inventory = self.get_object()
        return Response(
            {"preferred_connection_address": inventory.get_connection_address()}
        )
