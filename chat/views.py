# chat/views.py 
from django.http import HttpResponse, Http404, JsonResponse

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from .models import ChatRoom, Message
from account.models import Account
from matcher.models import Interest
from .models import PrivateChat, Message
from matcher.utils import find_matches_for_user

from kreviz.kafkaes import send_message
from django.core import serializers

from django.core.serializers.json import DjangoJSONEncoder
import json


def create_group_chats_based_on_interests():
    # Get all unique interests
    unique_interests = Interest.objects.all()

    with transaction.atomic():
        for interest in unique_interests:
            # Find users with the current interest
            users_with_interest = Account.objects.filter(interests=interest)

            # Check if a chat room for this interest already exists
            chat_room, created = ChatRoom.objects.get_or_create(
                interest=interest,
                defaults={'room_name': interest.name}
            )

            if created:
                # If the chat room is newly created, add all users with this interest
                chat_room.members.set(users_with_interest)
            else:
                # If the room already exists, update members if needed
                existing_members = set(chat_room.members.all())
                new_members = set(users_with_interest) - existing_members
                if new_members:
                    chat_room.members.add(*new_members)


# Call the function to create/update chat rooms
#create_group_chats_based_on_interests()



def chat_room_by_interest(request, interest_name=None):
    interest = get_object_or_404(Interest, name=interest_name)
    chat_room = get_object_or_404(ChatRoom, interest=interest)

    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            try:
                send_message('chat', {'message': message_content})
            except Exception as e:
                # Handle the exception (log it, inform the user, etc.)
                print(f"Error sending message to Kafka: {e}")

    messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')

    context = {
        'chat_room': chat_room,
        'room_name': chat_room.room_name,
        'messages': messages,
        'members': chat_room.members.all(),
    }

    return render(request, 'snippets/chat.html', context)



def chat_room_by_room_name(request, room_name):
    chat_room = get_object_or_404(ChatRoom, room_name=room_name)

# Retrieve messages for the chat room
    messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')

    context = {
        'chat_room': chat_room,
        'room_name': room_name,
        'messages': messages,
        'members': chat_room.members.all(),
    }

    return render(request, 'snippets/chat.html', context)



def priv_chat(request):
    user = request.user
    matches = find_matches_for_user(user)

    private_chats = PrivateChat.objects.filter(member1=user) | PrivateChat.objects.filter(member2=user)

    private_chats_messages = {}
    for chat in private_chats:
        messages = Message.objects.filter(private_chat=chat).order_by('timestamp')
        # Burada her mesajı bir Python sözlüğü olarak oluşturun
        private_chats_messages[chat.get_other_user(user).username] = [
            {'user': message.user.username, 'message': message.message, 'timestamp': message.timestamp}
            for message in messages
        ]

    # Tüm private_chats_messages sözlüğünü JSON formatına dönüştürün
    private_chats_messages_json = json.dumps(private_chats_messages, cls=DjangoJSONEncoder)

    context = {
        'matches': matches, 
        'private_chats_messages_json': private_chats_messages_json
    }

    private_chats_messages_json = json.dumps(private_chats_messages, cls=DjangoJSONEncoder)
    print(private_chats_messages_json)  # Bu, sunucu konsolunda JSON string'ini yazdıracaktır.


    return render(request, 'snippets/private.html', context)


    



def bubble_chat(request):
    username = request.GET.get('user', '')
    return render(request, 'snippets/bubble.html', {'username': username})
