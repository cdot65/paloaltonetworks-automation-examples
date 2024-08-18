# django_project/inventory/serializers.py
from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    preferred_connection_address = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            "id",
            "device_type",
            "hostname",
            "username",
            "connection_hostname",
            "connection_ipv4",
            "connection_ipv6",
            "preferred_connection_address",
        ]
        # Note: We're still not including the password field for security reasons

    def get_preferred_connection_address(self, obj):
        return obj.get_connection_address()
