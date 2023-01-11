from django.urls import path, re_path

from .import consumers

websocket_urlpatterns = [
    re_path('ws/<int:id>/', consumers.PersonalChatConsumer.as_asgi()),
]