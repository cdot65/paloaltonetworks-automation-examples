import django_filters
from .models import Job


class TaskResultFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            "status": [
                "exact",
                "icontains",
            ],
            "task_id": [
                "exact",
                "icontains",
            ],
            "created_at": [
                "gte",
                "lte",
            ],
        }
