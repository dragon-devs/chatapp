import json
from datetime import datetime

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
        now = datetime.now()

        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        name = data['name']
        room = data['room']
        pic = data['pic']

        date = now.strftime("%I:%M %p")

        await self.save_message(username, room, message, name, pic, date)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'name': name,
                'room': room,
                'pic': pic,
                'date': date,

            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        name = event['name']
        pic = event['pic']
        date = event['date']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
            'name': name,
            'pic': pic,
            'date': date,

        }))

    @database_sync_to_async
    def save_message(self, username, room, message, name, pic, date):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)
