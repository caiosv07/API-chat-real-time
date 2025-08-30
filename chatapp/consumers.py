import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatSala, ChatUser, Message

User = get_user_model()


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"ok": True}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=text_data)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sala_name = self.scope['url_route']['kwargs']['sala_name']
        self.sala_group_name = f'chat_{self.sala_name}'

        # Adiciona o usuário ao grupo da sala
        await self.channel_layer.group_add(
            self.sala_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove do grupo da sala
        await self.channel_layer.group_discard(
            self.sala_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        message_type = data.get('message_type', 'text')

        user = self.scope["user"]

        if not user.is_authenticated:
            await self.send(text_data=json.dumps({
                'error': 'Usuário não autenticado.'
            }))
            return

        # Salva a mensagem no banco
        msg_obj = await self.save_message(user, self.sala_name, message, message_type)

        # Envia para todos no grupo
        await self.channel_layer.group_send(
            self.sala_group_name,
            {
                'type': 'chat_message',
                'message': msg_obj.content,
                'sender': user.email,
                'message_type': msg_obj.message_type,
                'created_at': msg_obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'message_type': event['message_type'],
            'created_at': event['created_at']
        }))

    @database_sync_to_async
    def save_message(self, user, sala_name, content, message_type):
        sala, _ = ChatSala.objects.get_or_create(name=sala_name)
        return Message.objects.create(
            sala=sala,
            sender=user,
            content=content,
            message_type=message_type
        )
