# django_project/inventory/models.py
import uuid

from django.db import models
from django.core.validators import validate_ipv4_address, validate_ipv6_address


class Inventory(models.Model):
    DEVICE_CHOICES = [
        ("PAN-OS NGFW", "PAN-OS NGFW"),
        ("Panorama", "Panorama"),
    ]
    device_type = models.CharField(
        max_length=20,
        choices=DEVICE_CHOICES,
    )
    device_uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    hostname = models.CharField(
        max_length=255,
        help_text="Device hostname or FQDN",
    )
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    # Connection information
    connection_hostname = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Hostname or FQDN for SSH connection",
    )
    connection_ipv4 = models.GenericIPAddressField(
        protocol="IPv4",
        blank=True,
        null=True,
        validators=[validate_ipv4_address],
        help_text="IPv4 address for SSH connection",
    )
    connection_ipv6 = models.GenericIPAddressField(
        protocol="IPv6",
        blank=True,
        null=True,
        validators=[validate_ipv6_address],
        help_text="IPv6 address for SSH connection",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_type} - {self.hostname}"

    def get_connection_address(self):
        """
        Returns the preferred connection address in the order:
        IPv4 > IPv6 > Hostname > Default hostname
        """
        if self.connection_ipv4:
            return self.connection_ipv4
        elif self.connection_ipv6:
            return self.connection_ipv6
        elif self.connection_hostname:
            return self.connection_hostname
        else:
            return self.hostname
