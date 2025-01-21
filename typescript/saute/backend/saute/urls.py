from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (
    MessageViewSet,
    PanoramaViewSet,
    PanoramaPlatformViewSet,
    PanoramaExistsView,
    PrismaViewSet,
    FirewallPlatformViewSet,
    FirewallViewSet,
    FirewallExistsView,
    JobsViewSet,
    ScriptViewSet,
    UserViewSet,
    UserProfileView,
    execute_admin_report,
    execute_assurance_arp,
    execute_assurance_snapshot,
    execute_change_analysis,
    execute_chat,
    execute_create_script,
    execute_get_system_info,
    execute_upload_cert_chain,
    execute_pan_to_prisma,
    execute_assurance_readiness,
)

router = SimpleRouter()
router.register("ai/messages", MessageViewSet, basename="messages")
router.register("firewall/types", FirewallPlatformViewSet, basename="firewalltypes")
router.register("firewalls", FirewallViewSet, basename="firewalls")
router.register("panorama/types", PanoramaPlatformViewSet, basename="panorama_types")
router.register("panorama/inventory", PanoramaViewSet, basename="panorama_inventory")
router.register("prisma", PrismaViewSet, basename="prisma")
router.register("jobs", JobsViewSet, basename="jobs")
router.register("users", UserViewSet, basename="users")
router.register("scripts", ScriptViewSet, basename="scripts")

urlpatterns = router.urls

urlpatterns += [
    path("user-profile/", UserProfileView.as_view(), name="user_profile"),
    path(
        "ai/change-analysis",
        execute_change_analysis,
        name="execute_change_analysis",
    ),
    path(
        "ai/chat",
        execute_chat,
        name="execute_chat",
    ),
    path(
        "ai/create-script",
        execute_create_script,
        name="execute_create_script",
    ),
    path(
        "assessment/admin-report",
        execute_admin_report,
        name="execute_admin_report",
    ),
    path(
        "configuration/pan-to-prisma",
        execute_pan_to_prisma,
        name="execute_pan_to_prisma",
    ),
    path(
        "configuration/upload-cert-chain",
        execute_upload_cert_chain,
        name="execute_upload_cert_chain",
    ),
    path("firewall/exists", FirewallExistsView.as_view(), name="firewall_exists"),
    path("panorama/exists", PanoramaExistsView.as_view(), name="panorama_exists"),
    path(
        "automation/assurance-arp",
        execute_assurance_arp,
        name="execute_assurance_arp",
    ),
    path(
        "automation/assurance-readiness",
        execute_assurance_readiness,
        name="execute_assurance_readiness",
    ),
    path(
        "automation/assurance-snapshot",
        execute_assurance_snapshot,
        name="execute_assurance_snapshot",
    ),
    path(
        "report/get-system-info",
        execute_get_system_info,
        name="execute_get_system_info",
    ),
]
