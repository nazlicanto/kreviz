# chat/models.py

from django.db import models
from django.core.exceptions import ValidationError
# from account.models import Account


class ChatRoom(models.Model):

    room_name = models.CharField(max_length=255, unique=True)

    # Members of the chat room - many-to-many relationship with the User model
    members = models.ManyToManyField('account.Account')

    url = models.CharField(max_length=255, blank=True, null=True)

    # This links a chat room to a specific interest
    interest = models.ForeignKey('matcher.Interest', on_delete=models.CASCADE, null=True, blank=True)



class PrivateChat(models.Model):
    member1 = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='private_chats_as_member1')
    member2 = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='private_chats_as_member2')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp'),
        constraints = [models.UniqueConstraint(fields=['member1', 'member2'], name='unique_private_chat')]

    def get_other_user(self, user):
        if self.member1 == user:
            return self.member2
        else:
            return self.member1


    def __str__(self):
        return f"{self.member1.username} - {self.member2.username}"

    def clean(self):
        if self.member1 == self.member2:
            raise ValidationError("Private chat with yourself is not allowed.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)



class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # delivered = models.BooleanField(default=False) 
    private_chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('-timestamp',)

    def clean(self):
        if self.chat_room and self.private_chat:
            raise ValidationError("A message must be linked to either a group chat or a private chat, not both.")
        if not self.chat_room and not self.private_chat:
            raise ValidationError("A message must be linked to either a group chat or a private chat.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# private_chats_messages = serialize('json', Message.objects.filter(private_chat=chat), fields=('user', 'message', 'timestamp'))
    
