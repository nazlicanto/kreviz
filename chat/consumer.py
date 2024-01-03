# chat/consumers.py

import json
import logging
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer 
from channels.db import database_sync_to_async



logger = logging.getLogger(__name__)

user_channel_mapping = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            user_channel_mapping[self.user.username] = self.channel_name
        
        room_name = self.scope['url_route']['kwargs'].get('room_name')
        if room_name:
            self.room_name = room_name
            self.room_group_name = f"group_chat_{self.room_name}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        else:
            self.room_group_name = f"priv_{self.user.username}"

        await self.accept()
        logger.info(f"Connected to chat room {self.room_group_name}")
            

        



    # Deliver undelivered messages
    @database_sync_to_async
    def deliver_undelivered_messages(self, username):
        from .models import Message
        undelivered_messages = Message.objects.filter(user__username=username, delivered=False)
        for message in undelivered_messages:
            self.channel_layer.send(self.channel_name, {
                'type': 'chat_message',
                'message': message.message_text,
                
            })
            message.delivered = True
            message.save()



    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        private = text_data_json.get('private', False)
        recipient = text_data_json.get('recipient')
        username = self.user.username if self.user.is_authenticated else 'Anonymous'
        timestamp = datetime.now().strftime('%H:%M:%S')

        if private and recipient:
            # Handle private message
            
            await self.send_private_message({
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': str(timestamp),
                'recipient': recipient,
            })
        else:
            # Handle group message
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': str(timestamp),
            })

        await self.save_message(username, message, is_private=True, recipient=recipient)

# A database operation to save the message. 
# It's marked with @database_sync_to_async to be run asynchronously.
        
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
        logger.info(f"Sending message: {event['message']}")

    async def send_private_message(self, event):
        recipient = event['recipient']
        recipient_channel = await self.get_user_channel(recipient)

        if recipient_channel:
            # Send the message to the recipient's channel
            await self.channel_layer.send(recipient_channel, {
                'type': 'chat_message',
                'message': event['message'],
                'username': event['username'],
                'timestamp': event['timestamp'],
            })
            await self.mark_message_as_delivered(event['message'])
        else:
            await self.save_undelivered_message(event['message'], recipient)


        # Mark the message as delivered
    @database_sync_to_async
    def mark_message_as_delivered(self, message_text):
        from .models import Message
        Message.objects.filter(message=message_text).update(delivered=True)


    @database_sync_to_async
    def save_message(self, username, message_text, is_private=False, recipient=None):
        from .models import Message, PrivateChat, ChatRoom
        from account.models import Account

        sender = Account.objects.get(username=username) if username != 'Anonymous' else None

        if is_private and recipient:
            recipient_user = Account.objects.get(username=recipient)
            private_chat, created = PrivateChat.objects.get_or_create(
                member1=min(sender, recipient_user, key=lambda user: user.id),
                member2=max(sender, recipient_user, key=lambda user: user.id)
            )
            Message.objects.create(user=sender, private_chat=private_chat, message=message_text)
        else:
            # Genel sohbet odası için room_name kontrolü
            if hasattr(self, 'room_name'):
                chat_room = ChatRoom.objects.get(room_name=self.room_name)
                Message.objects.create(chat_room=chat_room, user=sender, message=message_text)
            else:
                # Burada, room_name tanımlı değilse yapılacak işlemi belirleyin.
                # Örneğin, bir hata mesajı loglayabilirsiniz veya başka bir işlem yapabilirsiniz.
                logger.error('Room name is not defined for a public chat message.')


    def get_current_chat_room(self):
        # Implementation logic to return the current chat room
        # For example, it could fetch a ChatRoom instance based on self.room_name
        from .models import ChatRoom
        try:
            return ChatRoom.objects.get(room_name=self.room_name)
        except ChatRoom.DoesNotExist:
            logger.error(f"ChatRoom not found: {self.room_name}")
            return None
        

    # Save the undelivered message
    @database_sync_to_async
    def save_undelivered_message(self, message_text, recipient_username):
        from .models import Message
        from account.models import Account

        recipient = Account.objects.get(username=recipient_username)
        # Assume you have a method to get the current chat room
        chat_room = self.get_current_chat_room()
        Message.objects.create(chat_room=chat_room, user=recipient, message=message_text, delivered=False)


# This method decides the group name for the chat. 
# It differentiates between one-to-one and group chats.

    def determine_room_group_name(self, room_name):
        if self.is_one_to_one_chat(room_name):
            group_name = self.get_one_to_one_room_group_name(room_name)
        else:
            group_name = f"group_chat_{room_name}"
        logger.info(f"Room group name determined: {group_name}")
        return group_name


    @database_sync_to_async
    def get_user_channel(self, username):
        return user_channel_mapping.get(username)


# Supposed to generate a unique room group name for one-to-one chats.
# One-to-one room names are composed of two user IDs separated by 
# an underscore, e.g., "user1_user2".
        
    @staticmethod
    def get_one_to_one_room_group_name(room_name):
        # Generate a unique room group name for one-to-one chat
        user_ids = sorted(room_name.split('_'))
        return f"one_to_one_chat_{'_'.join(user_ids)}"


    @database_sync_to_async
    def is_user_allowed(self, user, room_name):
        # Implement the logic to check if the user is allowed in the one-to-one chat room
        #check if user's ID is in the room_name
        user_id = str(user.id)
        return user_id in room_name.split('_')

        
        


    @staticmethod
    def is_one_to_one_chat(room_name):
        # Implement logic to determine if the chat is one-to-one based on room_name
        parts = room_name.split('_')
        return len(parts) == 2 and all(part.isdigit() for part in parts)
    

    

    


