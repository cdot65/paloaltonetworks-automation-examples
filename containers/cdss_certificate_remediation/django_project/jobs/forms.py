# django_project/jobs/forms.py

from django import forms
from .models import Automation
from django_project.inventory.models import Inventory


class AutomationForm(forms.ModelForm):
    hostnames = forms.ModelMultipleChoiceField(
        queryset=Inventory.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )
    automation_script = forms.ChoiceField(
        choices=Automation.SCRIPT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    dry_run = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.RadioSelect(
            choices=(
                (
                    True,
                    "Yes",
                ),
                (
                    False,
                    "No",
                ),
            )
        ),
    )

    class Meta:
        model = Automation
        fields = [
            "hostnames",
            "automation_script",
            "dry_run",
        ]
