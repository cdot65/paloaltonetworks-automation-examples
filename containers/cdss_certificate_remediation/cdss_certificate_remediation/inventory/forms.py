# cdss_certificate_remediation/inventory/forms.py
from django import forms
from .models import Inventory


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            "device_type",
            "hostname",
            "username",
            "password",
            "connection_hostname",
            "connection_ipv4",
            "connection_ipv6",
        ]
        widgets = {
            "device_type": forms.Select(attrs={"class": "form-select"}),
            "hostname": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter device hostname or FQDN",
                }
            ),
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Device Username"}
            ),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "connection_hostname": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter specific hostname for SSH connection (optional)",
                }
            ),
            "connection_ipv4": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter IPv4 address for SSH connection (optional)",
                }
            ),
            "connection_ipv6": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter IPv6 address for SSH connection (optional)",
                }
            ),
        }
