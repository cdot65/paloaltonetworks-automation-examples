from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "hostname",
        "device_type",
        "device_uuid",
    )
    list_filter = ("device_type",)
    search_fields = (
        "hostname",
        "device_type",
        "device_uuid",
    )
    readonly_fields = (
        "device_uuid",
        "created_at",
        "updated_at",
    )
