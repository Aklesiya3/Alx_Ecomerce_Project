from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.register_url = reverse('register')
		self.token_url = reverse('token_obtain_pair')
		self.refresh_url = reverse('token_refresh')
		self.logout_url = reverse('logout')
		self.profile_url = reverse('profile')

	def test_register_and_login_and_profile_and_logout(self):
		# Register
		data = {'email': 'tester@example.com', 'password': 'strongpass'}
		resp = self.client.post(self.register_url, data, format='json')
		if resp.status_code != 201:
			print('REGISTER RESPONSE:', resp.status_code, resp.data)
		self.assertEqual(resp.status_code, 201)

		# Obtain tokens
		resp = self.client.post(self.token_url, {'email': 'tester@example.com', 'password': 'strongpass'}, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('access', resp.data)
		self.assertIn('refresh', resp.data)
		access = resp.data['access']
		refresh = resp.data['refresh']

		# Access profile
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		resp = self.client.get(self.profile_url)
		self.assertEqual(resp.status_code, 200)

		# Logout (blacklist refresh)
		resp = self.client.post(self.logout_url, {'refresh': refresh}, format='json')
		self.assertIn(resp.status_code, (200, 205))

	def test_custom_login_endpoint(self):
		# Register user
		data = {'email': 'loginuser@example.com', 'password': 'strongpass'}
		resp = self.client.post(self.register_url, data, format='json')
		self.assertEqual(resp.status_code, 201)

		# Login using custom login endpoint
		resp = self.client.post(reverse('login'), {'email': 'loginuser@example.com', 'password': 'strongpass'}, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('access', resp.data)
		self.assertIn('refresh', resp.data)
		self.assertIn('user', resp.data)


# Create your tests here.
