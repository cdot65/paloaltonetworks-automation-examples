# django_project/task_results/models.py

from django.db import models


class TaskResult(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task {self.task_id}: {self.status}"
