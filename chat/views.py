from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
import json

from django.views import View

from chat.models import Room, Message


class Index(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.exclude(username=request.user.username)

        return render(request, 'index.html', {
            'users': users
        })


class RoomView(LoginRequiredMixin, View):
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


class UserRegister(View):
    def post(self, request):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return redirect('index')

    def get(self, request):
        return render(request, 'register.html', {})


class UserLogin(View):
    def post(self, request):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        u = authenticate(username=username, password=password)
        if u:
            login(request, u)
        else:
            return render(request, 'login.html', {})
        return redirect('index')

    def get(self, request):
        return render(request, 'login.html', {})
