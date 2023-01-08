import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User

from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']["room_name"]
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        name = data['name']
        room = data['room']


        await self.save_message(username, room, message, name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'name': name,
                'room': room,

            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        name = event['name']


        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
            'name': name,

        }))

    @sync_to_async
    def save_message(self, username, room, message, name):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        name = user.profile.name

        Message.objects.create(user=user, room=room, content=message)


