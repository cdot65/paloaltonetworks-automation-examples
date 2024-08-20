from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "task_id", "status", "result", "created_at", "updated_at"]
        read_only_fields = ["id", "task_id", "created_at", "updated_at"]
