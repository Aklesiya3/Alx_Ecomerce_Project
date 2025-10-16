from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()


class ProductAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.list_url = reverse('products-list')
		self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')

	def test_public_list_and_admin_create(self):
		# Public can list
		resp = self.client.get(self.list_url)
		self.assertEqual(resp.status_code, 200)

		# Unauthenticated create returns 401
		resp = self.client.post(self.list_url, {'name': 'P1', 'price': '10.00', 'stock': 5}, format='json')
		self.assertEqual(resp.status_code, 401)

		# Admin can create
		self.client.force_authenticate(self.admin)
		resp = self.client.post(self.list_url, {'name': 'P1', 'price': '10.00', 'stock': 5}, format='json')
		self.assertEqual(resp.status_code, 201)
		pid = resp.data['id']

		# Retrieve product
		resp = self.client.get(reverse('products-detail', args=[pid]))
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.data['name'], 'P1')
