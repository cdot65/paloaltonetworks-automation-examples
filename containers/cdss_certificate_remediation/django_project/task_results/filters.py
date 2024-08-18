import django_filters
from .models import TaskResult


class TaskResultFilter(django_filters.FilterSet):
    class Meta:
        model = TaskResult
        fields = {
            "status": ["exact", "icontains"],
            "task_id": ["exact", "icontains"],
            "created_at": ["gte", "lte"],
        }
