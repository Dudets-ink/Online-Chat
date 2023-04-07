from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.Chat.as_view(), name='chat'),
    path('chat/<str:room_name>/', views.CharRoom.as_view(), name='chat_room'),
]
