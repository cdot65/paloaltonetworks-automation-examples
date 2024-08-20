import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            "status": [
                "exact",
                "icontains",
            ],
            "job_id": [
                "exact",
                "icontains",
            ],
            "created_at": [
                "gte",
                "lte",
            ],
        }
