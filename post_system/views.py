from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import *
from .forms import *

class Index(ListView):
	model = Post
	context_object_name = "posts"
	template_name = "post_system/index.html"


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = "form.html"
	form_class = PostCreateForm

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

	def get_success_url(self) -> str:
		return reverse_lazy("post:index")


class PostUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
	model = Post
	template_name = "form.html"
	context_object_name = "post"
	form_class = PostCreateForm

	def get_success_url(self) -> str:
		return reverse_lazy("post:index")


class PostDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
	model = Post
	template_name = "form.html"

	def get_success_url(self) -> str:
		return reverse_lazy("post:index")

# class CommentLikeToggle(LoginRequiredMixin, View):
# 	def post(self, request, *args, **kwargs) :
# 		comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
# 		like_qs = Like.objects.filter(comment=comment, user=request.user)
# 		if like_qs.exists():
# 			like_qs.delete()
# 		else:
# 			Like.objects.create(comment=comment, user=request.user)
# 		return redirect("task-tracker:task-details", dashboard_pk=self.kwargs['dashboard_pk'],pk=self.kwargs['task_pk'])
	
# class DeleteCommentView(LoginRequiredMixin,UserIsOwnerMixin,DeleteView):
# 	model = Comment
# 	template_name = "form.html"
	
# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:task-details",  kwargs={'dashboard_pk': self.kwargs['dashboard_pk'],"pk": self.kwargs['task_pk']})

# class UpdateCommentView(LoginRequiredMixin,UserIsOwnerMixin,UpdateView):
# 	model = Comment
# 	template_name = "form.html"
# 	context_object_name = "comment"
# 	form_class = CommentCreateForm

# 	def get_success_url(self) -> str:
# 		return reverse_lazy("task-tracker:task-details",  kwargs={'dashboard_pk': self.kwargs['dashboard_pk'],"pk": self.kwargs['task_pk']})