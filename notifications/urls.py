from django.urls import path
from .views import * 

urlpatterns = [
	path('<int:pk>', NotificationView.as_view(), name='notifications'),
	path('mark-as-read', mark_notifications_as_read, name='mark_notifications_as_read'),
]
