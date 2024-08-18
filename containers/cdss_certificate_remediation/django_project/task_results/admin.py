from django.contrib import admin
from .models import TaskResult


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ("task_id", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("task_id", "status")
    readonly_fields = ("task_id", "created_at", "updated_at")
