# django_project/jobs/models.py

from django.db import models
from django_project.inventory.models import Inventory


class Job(models.Model):
    job_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job {self.job_id}: {self.status}"


class JobLog(models.Model):
    job = models.ForeignKey(
        Job,
        related_name="logs",
        on_delete=models.CASCADE,
    )
    log = models.JSONField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for Job {self.job.job_id} at {self.created_at}"


class Automation(models.Model):
    SCRIPT_CHOICES = [
        (
            "script1",
            "Script 1",
        ),
        (
            "script2",
            "Script 2",
        ),
    ]

    hostnames = models.ManyToManyField(
        Inventory,
        related_name="automations",
        blank=True,
    )
    automation_script = models.CharField(
        max_length=255,
        choices=SCRIPT_CHOICES,
    )
    dry_run = models.BooleanField(default=True)
    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Automation {self.id}: {self.automation_script}"
