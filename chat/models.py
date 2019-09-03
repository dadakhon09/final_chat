from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    text = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.room.sender} - {self.room.receiver}'
