from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from chat.models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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

        room_id_sender = pow(2, int(sender.id)) * pow(3, int(receiver.id))
        room_id_receiver = pow(2, int(receiver.id)) * pow(3, int(sender.id))

        if Room.objects.filter(room_name=f'room_{room_id_sender}').exists():
            room = Room.objects.get(room_name=f'room_{room_id_sender}')

        else:
            room = Room.objects.get(room_name=f'room_{room_id_receiver}')

        m = Message.objects.create(sender=sender, receiver=receiver, text=message, room=room)

        await self.channel_layer.group_send(
            str(receiver.id),
            {
                'type': 'chat_message',
                'message': m.text,
                'sender': sender.username,
                'receiver_username': receiver.username,
                'created_minute': int(m.created.minute)
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_username = event['sender']
        receiver_username = event.get('receiver_username')
        created_minute = event['created_minute']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender_username,
            'receiver_username': receiver_username,
            'created_minute': created_minute
        }))
