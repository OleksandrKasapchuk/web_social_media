from django import forms
from .models import *


class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['media', 'content']
		widjets = {
			"media": forms.FileInput()
		}

class CommentCreateForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']
