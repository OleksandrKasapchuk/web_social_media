from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('<int:chat_id>/', chat_detail, name='chat_detail'),
    path('start/<int:user_id>/', start_chat, name='start_chat'),
]
