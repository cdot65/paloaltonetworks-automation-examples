from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "device_uuid",
        "device_type",
        "hostname",
        "connection_hostname",
    )
    list_filter = (
        "device_type",
        "hostname",
        "connection_hostname",
    )
    search_fields = (
        "device_uuid",
        "device_type",
        "hostname",
        "connection_hostname",
    )
    readonly_fields = (
        "device_uuid",
        "created_at",
        "updated_at",
    )
