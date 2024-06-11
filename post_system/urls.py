from django.urls import path
import post_system.views as post_views

urlpatterns = [
	path('', post_views.Index.as_view(), name='index'),
]