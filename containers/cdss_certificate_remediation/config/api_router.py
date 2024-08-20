# config/api_router.py
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from django_project.users.api.views import UserViewSet
from django_project.inventory.api_views import InventoryViewSet
from django_project.jobs.api_views import JobViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("inventory", InventoryViewSet)
router.register("jobs", JobViewSet)

app_name = "api"
urlpatterns = router.urls
