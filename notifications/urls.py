from django.urls import path
from .views import * 

urlpatterns = [
	path('notifications/<int:pk>', NotificationView.as_view(), name='notifications'),
]
