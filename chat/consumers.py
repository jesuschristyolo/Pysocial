import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from users.models import User
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json, 'text_data')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message",
                                   "message": text_data_json["message"],
                                   "sender": text_data_json["sender"],
                                   "sender_pk": text_data_json["sender_pk"],
                                   "receiver_pk": text_data_json["receiver_pk"],
                                   "channel_pk": text_data_json["channel_pk"],
                                   }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print(event)
        message = event["message"]
        sender = event["sender"]

        user = await sync_to_async(User.objects.get)(username=sender)
        sender_photo = user.photo.url
        print(sender_photo)

        await sync_to_async(Message.create_object)(
            new_sender_pk=event["sender_pk"],
            new_receiver_pk=event["receiver_pk"],
            new_content=message,
            channel_pk=event["channel_pk"]
        )

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender, 'sender_photo': sender_photo}))
