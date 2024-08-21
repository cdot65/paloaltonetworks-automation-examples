from django.urls import path
from . import views

app_name = "health"

urlpatterns = [
    path("", views.health_check, name="health"),
]
