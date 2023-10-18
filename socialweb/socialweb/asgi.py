"""
ASGI config for socialweb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from application.chat import consumers

from django.urls import re_path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialweb.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(routes=[re_path(r'^ws/\w+/', consumers.ChatConsumer.as_asgi())])
})
