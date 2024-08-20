# django_project/jobs/models.py

from django.db import models


class Job(models.Model):
    job_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job {self.job_id}: {self.status}"
