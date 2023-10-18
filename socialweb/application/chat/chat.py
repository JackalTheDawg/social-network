import json
from application.models import *
from django.utils import timezone
from application.models import CustomUser, ChatModel, Message
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import asyncio

class Chat:
    @classmethod
    def start_chat(self, page_id, sender_id):
        chat = ChatModel.objects.filter(members__in=[sender_id, page_id])
        if chat.exists():
            return chat[0].id
        else:
            create_chat = ChatModel.objects.create()
            create_chat.members.set([sender_id, page_id])
            return create_chat.id

    def get_messages(self, chat_id):
        message_obj = Message.objects.filter(chat=chat_id)
        context = []
        if message_obj.exists():
            for message in message_obj:
                context.append(message)

        return context



