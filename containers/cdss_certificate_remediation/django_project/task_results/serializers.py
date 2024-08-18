from rest_framework import serializers
from .models import TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ["id", "task_id", "status", "result", "created_at", "updated_at"]
        read_only_fields = ["id", "task_id", "created_at", "updated_at"]
