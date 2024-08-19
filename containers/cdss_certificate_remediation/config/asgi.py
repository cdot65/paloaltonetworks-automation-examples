import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django_project.inventory import routing as inventory_routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(inventory_routing.websocket_urlpatterns)
        ),
    }
)
