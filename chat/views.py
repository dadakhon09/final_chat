from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from django.views import View


class Index(View):
    def get(self, request):
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'index.html', {'users': users})


class Room(View):
    def get(self, request, room_name):
    	return render(request, 'room.html', {
            'sender': mark_safe(json.dumps(self.request.user.username)),
            'room_name_json': mark_safe(json.dumps(room_name))
        })
