from django.db import models
from auth_system.models import CustomUser


class Room(models.Model):
	name = models.CharField(max_length=100)


class Message(models.Model):
	content = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)