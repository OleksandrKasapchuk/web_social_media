from django.urls import path
import post_system.views as post_views

urlpatterns = [
	path('', post_views.Index.as_view(), name='index'),
	path('add_post/', post_views.PostCreateView.as_view(), name='add_post'),
	path('update_post/<int:pk>', post_views.PostUpdateView.as_view(), name='update_post'),
	path('delete_post/<int:pk>', post_views.PostDeleteView.as_view(), name='delete_post'),
]

app_name = 'post' 