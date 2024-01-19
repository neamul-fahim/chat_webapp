import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message
from channels.db import database_sync_to_async


User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    # @database_sync_to_async
    # def get_existing_messages(self):
    #     # Fetch existing messages for the room
    #     return Message.objects.filter(room_name=self.roomGroupName).order_by('timestamp')

    # @database_sync_to_async
    # def send_existing_messages(self, messages):
    #     # Send existing messages to the connecting user
    #     for message in messages:
    #         print(message)
    #         self.send(text_data=json.dumps({
    #             "message": message.content,
    #             "username": message.sender.username,
    #         }))

    async def connect(self):
        self.user_id = int(self.scope['user'].id)
        print(f"User connected with ID: {self.user_id}")
        self.receiver_id = int(self.scope['url_route']['kwargs']['userId'])
        print(f"Receiver connected: {self.receiver_id}")

        sorted_ids = sorted([self.user_id, self.receiver_id])
        self.roomGroupName = f"chat_{sorted_ids[0]}_{sorted_ids[1]}"

        # self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )

        # messages = await self.get_existing_messages()
        # await self.send_existing_messages(messages)

        await self.accept()
        # Add this line

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            # self.channel_layer
            self.channel_name  # Corrected line

        )

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, message, room_name):
        return Message.objects.create(sender=sender, receiver=receiver, content=message, room_name=room_name)

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        sender = await self.get_user(self.user_id)
        receiver = await self.get_user(self.receiver_id)

        # Save the message to the database
        message = await self.save_message(sender, receiver, message, self.roomGroupName)
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
            })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message.content, "username": username}))
