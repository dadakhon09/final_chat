from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from chat.models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        await self.channel_layer.group_add(
            self.receiver_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.receiver_id,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = User.objects.get(username=text_data_json['sender'])
        receiver = User.objects.get(username=text_data_json['receiver'])
        room_name = text_data_json['room_name']

        if room_name == f'to_{receiver.id}':
            room = Room.objects.get(room_name=room_name)
        elif room_name ==f'to_{sender.id}':
            room = Room.objects.get(room_name=f'to_{sender.id}')

        Message.objects.create(sender=sender, receiver=receiver, text=message, room=room)

        await self.channel_layer.group_send(
            receiver.id,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

        # await self.send(text_data=json.dumps({
        #     'message': message,
        #     'sender': sender.username,
        # }))

    async def chat_message(self, event):
        message = event['message']
        sender_username = event['sender']
    
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender_username,
        }))
