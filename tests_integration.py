from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from Product.models import Product
from User.models import Address

User = get_user_model()


class IntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='int1', email='int1@example.com', password='pass')
        self.client.force_authenticate(self.user)
        # create products
        self.p1 = Product.objects.create(name='Prod A', price='2.50', stock=10)
        self.p2 = Product.objects.create(name='Prod B', price='5.00', stock=3)

    def test_cart_order_and_review_flow(self):
        # Add to cart
        cart_url = reverse('cart-list-create')
        resp = self.client.post(cart_url, {'product_id': self.p1.id, 'quantity': 2}, format='json')
        self.assertEqual(resp.status_code, 201)

        # Add second product
        resp = self.client.post(cart_url, {'product_id': self.p2.id, 'quantity': 1}, format='json')
        self.assertEqual(resp.status_code, 201)

        # Create address for user
        addr = Address.objects.create(user=self.user, line1='123 Main', state='X', city='Y', country='Z')
        self.user.address = addr
        self.user.save()

        # Ensure cart has items
        from Cart.models import CartItem
        self.assertTrue(CartItem.objects.filter(user=self.user).exists(), 'Cart is unexpectedly empty before order')

        # Create order
        order_create = reverse('order-create')
        print('DEBUG user.address:', self.user.address)
        print('DEBUG cart items:', list(CartItem.objects.filter(user=self.user).values('product_id', 'quantity')))
        resp = self.client.post(order_create)
        print('DEBUG ORDER RESPONSE', resp.status_code, getattr(resp, 'data', None))
        self.assertEqual(resp.status_code, 201, f'Order creation failed: {resp.status_code} {resp.data}')

        # After order, stock decreased
        self.p1.refresh_from_db(); self.p2.refresh_from_db()
        self.assertEqual(self.p1.stock, 8)
        self.assertEqual(self.p2.stock, 2)

        # Post a review for p1
        review_url = reverse('product-reviews', args=[self.p1.id])
        resp = self.client.post(review_url, {'rating': 5, 'comment': 'Nice'}, format='json')
        print('DEBUG REVIEW POST:', resp.status_code, getattr(resp, 'data', None))
        self.assertEqual(resp.status_code, 201, f'Review post failed: {resp.status_code} {resp.data}')

        # List reviews
        resp = self.client.get(review_url)
        print('DEBUG REVIEW LIST:', resp.status_code, getattr(resp, 'data', None))
        self.assertEqual(resp.status_code, 200, f'Review list failed: {resp.status_code} {resp.data}')
        self.assertTrue(len(resp.data) >= 1)
