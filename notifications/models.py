# models.py
from django.db import models
from auth_system.models import CustomUser
from post_system.models import *
from chat.models import *


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('post', 'Post'),
        ('comment', 'Comment'),
        ('chat', 'Chat'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.message}'