from django.test import TestCase
from .models import Post
from auth_system.models import CustomUser


class IndexTest(TestCase):
	def test_index_access(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)


class AddPostTest(TestCase):
	def test_index_access(self):
		response = self.client.get('/add-post/')
		self.assertEqual(response.status_code, 200)


class PostModelTest (TestCase):
	def test_create_post (self):
		post = Post.objects.create(
		content="Test post 1",
		user=CustomUser.objects.create(username="admin", password="12345678"),
		media='media/post_media/Believe.jpg'
		)
		self.assertEqual(post.content, "Test post 1")
		self.assertEqual(post.user.username, "admin")
		self.assertTrue(post.media)