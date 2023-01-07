import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        pass
