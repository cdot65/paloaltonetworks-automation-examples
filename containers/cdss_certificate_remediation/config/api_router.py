# config/api_router.py
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from cdss_certificate_remediation.users.api.views import UserViewSet
from cdss_certificate_remediation.inventory.api_views import InventoryViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("inventory", InventoryViewSet)

app_name = "api"
urlpatterns = router.urls
