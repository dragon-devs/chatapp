
import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path

from chat.consumers import *
from room.consumers import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', PersonalChatConsumer.as_asgi()),
            path('ws/<str:room_name>/', ChatConsumer.as_asgi()),


        ])
    )
})
