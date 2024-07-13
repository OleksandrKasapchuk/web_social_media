from django.urls import path
from .views import *


urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('<int:pk>/', chat_detail, name='chat_detail'),
    path('start/<int:user_id>/', start_chat, name='start_chat'),
	path('<int:chat_id>/delete_message/<int:pk>', DeleteMessageView.as_view(), name='delete_message'),
]

app_name = "chat"