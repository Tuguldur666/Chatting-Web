from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='chatrooms')
    def __str__(self):
        return self.name or f"Room {self.id} with {self.members.count()} members"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
