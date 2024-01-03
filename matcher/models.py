# matcher/models.py

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.apps import apps


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    interest_mapping = {
        "Yoga" : 1,
        "Writing":2,
        "Hiking" : 3,
        "Cooking": 4,
        "3D Printing": 5,
    }

    def __str__(self):
        return self.name
    
@receiver(m2m_changed)
def add_user_to_chat_room(sender, instance, action, pk_set, **kwargs):
    if sender == apps.get_model('account', 'Account').interests.through:
        if action == "post_add":
            ChatRoom = apps.get_model('chat', 'ChatRoom')
            for interest_pk in pk_set:
                interest = Interest.objects.get(pk=interest_pk)
                chat_room, created = ChatRoom.objects.get_or_create(
                    interest=interest,
                    defaults={'room_name': f'Chat for {interest.name}'}
                )
                chat_room.members.add(instance)
