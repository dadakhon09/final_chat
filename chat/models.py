from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        db_table = 'rooms'

    def __str__(self):
        return self.room_name


class Message(models.Model):
    text = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        db_table = 'messages'

    def __str__(self):
        return self.text
