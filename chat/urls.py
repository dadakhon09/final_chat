from django.urls import path

from chat.views import Index, RoomView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<int:receiver_id>/', RoomView.as_view(), name='room'),
]
