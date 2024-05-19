from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
import os
from .models import (
    Panorama,
    PanoramaPlatform,
    Prisma,
    Firewall,
    FirewallPlatform,
    Jobs,
    Message,
    Script,
)


class PanoramaPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanoramaPlatform
        fields = (
            "id",
            "name",
        )


class PanoramaSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source="platform.name", read_only=True)
    ipv6_address = serializers.IPAddressField(
        protocol="IPv6",
        allow_blank=True,
        required=False,
        allow_null=True,
    )

    def create(self, validated_data):
        return Panorama.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Panorama
        fields = (
            "api_key",
            "author",
            "created_at",
            "hostname",
            "ipv4_address",
            "ipv6_address",
            "notes",
            "platform",
            "uuid",
        )


class PrismaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prisma
        fields = (
            "id",
            "tenant_name",
            "client_id",
            "client_secret",
            "tsg_id",
            "author",
            "created_at",
        )


class FirewallSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source="platform.name", read_only=True)
    ipv6_address = serializers.IPAddressField(
        protocol="IPv6",
        allow_blank=True,
        required=False,
        allow_null=True,
    )

    def create(self, validated_data):
        return Firewall.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Firewall
        fields = (
            "api_key",
            "author",
            "created_at",
            "hostname",
            "ipv4_address",
            "ipv6_address",
            "notes",
            "platform",
            "uuid",
        )


class FirewallPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirewallPlatform
        fields = (
            "id",
            "name",
            "vendor",
        )


class JobsSerializer(serializers.ModelSerializer):
    task_id = serializers.CharField(read_only=True)  # Add the task_id field

    class Meta:
        model = Jobs
        fields = (
            "task_id",
            "job_type",
            "author",
            "created_at",
            "json_data",
        )


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "profile_image",
        )
        read_only_fields = ("is_staff", "is_superuser")

    def get_profile_image(self, obj):
        if obj.profile_image:
            return settings.MEDIA_URL + str(obj.profile_image)
        return None


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class ScriptSerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True, required=False)
    file_content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Script
        fields = "__all__"

    def get_file_content(self, obj):
        file_path = os.path.join(settings.SCRIPTS_BASE_PATH, obj.file.name)
        try:
            with open(file_path) as f:
                return f.read()
        except FileNotFoundError:
            print("FileNotFoundError for file path: ", file_path)
            return "File not found"

    def update(self, instance, validated_data):
        file_path = os.path.join(settings.SCRIPTS_BASE_PATH, instance.file.name)
        if "content" in validated_data:
            with open(file_path, "w") as f:
                f.write(validated_data.pop("content"))

        return super().update(instance, validated_data)
