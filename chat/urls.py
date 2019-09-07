from django.contrib.auth.views import LogoutView
from django.urls import path

from chat.views import Index, RoomView, UserRegister, UserLogin

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<int:receiver_id>/', RoomView.as_view(), name='room'),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]
