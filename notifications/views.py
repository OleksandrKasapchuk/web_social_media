from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification


class NotificationView(LoginRequiredMixin,ListView):
	model = Notification
	template_name = 'notifications/notifications.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["notifications"] = Notification.objects.filter(user=self.kwargs["pk"])
		return context

@login_required
def mark_notifications_as_read(request):
    if request.method == 'POST':
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)