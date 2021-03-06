import asyncio
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def wtf(sender, instance, created, **kwargs):
    if created:
        up = UserProfile(user=instance)
        up.save()


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        db_table = 'rooms'

    def __str__(self):
        return self.room_name


class Message(models.Model):
    text = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        db_table = 'messages'

    def __str__(self):
        return self.text


@receiver(post_save, sender=Message)
def send(instance, **kwargs):
    from channels.layers import get_channel_layer
    loop = asyncio.get_event_loop()
    layer = get_channel_layer()
    time = datetime.today().minute - instance.created.minute
    loop.create_task(layer.group_send(str(instance.sender.id), {
        'type': 'chat_message',
        'message': instance.text,
        'sender': instance.sender.username,
        'created_minute': time
    }))
