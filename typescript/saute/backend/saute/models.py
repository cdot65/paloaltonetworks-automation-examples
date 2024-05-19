import uuid
from django.conf import settings
from django.db import models
from django.core.validators import (
    FileExtensionValidator,
)


class PanoramaPlatform(models.Model):
    """
    Represents a specific type of Panorama.

    Each instance of the PanoramaPlatform class holds information about a distinct platform of Panorama.

    Fields:
    - name: The unique name of the PanoramaPlatform.
    """

    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        """
        This function returns the name of the PanoramaPlatform as a string representation.
        """
        return self.name


class Panorama(models.Model):
    """
    Panorama appliance.

    Each instance of the Panorama class holds information about a distinct Panorama appliance.

    Fields:
    - hostname: The unique name of the Panorama appliance.
    """

    api_key = models.CharField(max_length=1024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True, null=True)
    ipv4_address = models.GenericIPAddressField()
    ipv6_address = models.GenericIPAddressField(protocol="IPv6", blank=True, null=True)
    platform = models.ForeignKey(
        PanoramaPlatform, blank=True, null=True, on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.hostname


class Prisma(models.Model):
    tenant_name = models.CharField(max_length=100, unique=True)
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    tsg_id = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tenant_name


class Jobs(models.Model):
    task_id = models.CharField(max_length=255, unique=True, primary_key=True)
    job_type = models.CharField(max_length=1024)
    json_data = models.JSONField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_id


class FirewallPlatform(models.Model):
    """
    Represents a specific type of firewall.

    Each instance of the FirewallPlatform class holds information about a distinct platform of firewall.

    Fields:
    - hostname: The unique name of the FirewallPlatform.
    """

    name = models.CharField(max_length=32, unique=True)
    vendor = models.CharField(max_length=32)

    def __str__(self):
        """
        This function returns the name of the FirewallPlatform as a string representation.
        """
        return self.name


class Firewall(models.Model):
    """
    Firewall appliance.

    Each instance of the Firewall class holds information about a distinct firewall appliance.

    Fields:
    - hostname: The unique name of the firewall appliance.
    """

    api_key = models.CharField(max_length=1024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=100, unique=True)
    notes = models.TextField(blank=True, null=True)
    ipv4_address = models.GenericIPAddressField()
    ipv6_address = models.GenericIPAddressField(protocol="IPv6", blank=True, null=True)
    platform = models.ForeignKey(
        FirewallPlatform, blank=True, null=True, on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.hostname


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, unique=True, editable=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations_author",
    )
    AGENT_CHOICES = [
        ("ChatGPT v3.5", "ChatGPT v3.5"),
        ("ChatGPT v4", "ChatGPT v4"),
        ("LLaMa", "LLaMa"),
    ]
    llm = models.CharField(max_length=15, choices=AGENT_CHOICES, default="ChatGPT v4")
    PERSONAS = (
        ("Herbert", "Herbert"),
        ("Jamie", "Jamie"),
        ("Other", "Other"),
    )
    persona = models.CharField(max_length=10, choices=PERSONAS, default="Other")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {self.author} and {self.llm}"


class Message(models.Model):
    index = models.PositiveIntegerField()
    ROLE_CHOICES = [
        ("user", "User"),
        ("bot", "Bot"),
    ]
    role = models.CharField(max_length=4, choices=ROLE_CHOICES, default="user")
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.content


class Script(models.Model):
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(
        upload_to="scripts/",
        validators=[FileExtensionValidator(allowed_extensions=["py"])],
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
