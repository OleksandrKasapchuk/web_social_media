from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
	bio = models.TextField(null=True, blank=True)
	avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
	
	def __str__(self):
		return self.username