"""
ASGI config for waiching project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels import routing
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from waiching import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webSocket.settings')

# application = get_asgi_application()


# 支持http请求和websocket请求
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(routings.websocket_urlpatterns)
})
