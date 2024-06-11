from django.db import models
from auth_system.models import *


class Post(models.Model):
	content = models.TextField()
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
	date_published = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user} - {self.date_published}"

	class Meta:
		ordering = ('date_published',)


class Comment(models.Model):
	content = models.CharField(max_length=100)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	date_published = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user} - {self.date_published}"
	
	class Meta:
		ordering = ('date_published',)


class Like(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes")
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

	class Meta:
		unique_together = ('user', 'post')