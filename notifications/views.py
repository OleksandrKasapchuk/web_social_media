from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import *
from notifications.models import Notification
from django.views.generic import View, ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin



class NotificationView(ListView):
	model = Notification
	template_name = 'notifications/notifications.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["notifications"] = Notification.objects.filter(user=self.kwargs["pk"])
		return context