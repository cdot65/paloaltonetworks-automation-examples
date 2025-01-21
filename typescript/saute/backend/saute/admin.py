from django.contrib import admin


from .models import (
    Firewall,
    FirewallPlatform,
    Jobs,
    Panorama,
    Prisma,
)


class PanoramaAdmin(admin.ModelAdmin):
    list_display = (
        "hostname",
        "ipv4_address",
        "ipv6_address",
        "api_key",
    )


class PrismaAdmin(admin.ModelAdmin):
    list_display = (
        "tenant_name",
        "client_id",
        "tsg_id",
    )


admin.site.register(Panorama, PanoramaAdmin)
admin.site.register(Prisma, PrismaAdmin)
