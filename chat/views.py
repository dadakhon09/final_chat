from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json

from django.views import View

from chat.models import Room, Message


class Index(View):
    def get(self, request):
        users = User.objects.exclude(username=request.user.username)

        return render(request, 'index.html', {
            'users': users
        })


class RoomView(View):
    def get(self, request, receiver_id):
        users = User.objects.exclude(username=request.user.username)

        receiver = get_object_or_404(User, id=receiver_id)

        if receiver != request.user:
            room, _ = Room.objects.get_or_create(sender=request.user, receiver=receiver,
                                                 room_name=f'{request.user}-and-{receiver}')
        else:
            return HttpResponse("You can't chat to yourself")

        messages = Message.objects.filter(room=room)  # .order_by('-created')[:5][::-1]

        return render(request, 'room.html', {
            'users': users,
            'messages': messages,
            'sender': mark_safe(json.dumps(self.request.user.username)),
            'receiver': receiver,
            'room_name_json': mark_safe(json.dumps(room.room_name))
        })
        
