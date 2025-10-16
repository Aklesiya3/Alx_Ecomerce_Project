from decimal import Decimal
from django.db import transaction
from django.db.models import F
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from Cart.models import CartItem
from Product.models import Product
from rest_framework.exceptions import ValidationError

class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        # Ensure user has an address before creating order
        if not getattr(user, 'address', None):
            return Response({"detail": "User address required to place order."}, status=status.HTTP_400_BAD_REQUEST)
        cart_items = CartItem.objects.select_related('product').filter(user=user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            product_ids = [ci.product_id for ci in cart_items]
            products_qs = Product.objects.select_for_update().filter(id__in=product_ids)
            pmap = {p.id: p for p in products_qs}

            total = Decimal('0.00')
            order = Order.objects.create(user=user, status='pending', total_price=0)

            for ci in cart_items:
                prod = pmap.get(ci.product_id)
                if not prod:
                    raise ValidationError(f"Product {ci.product_id} not found")
                if prod.stock < ci.quantity:
                    raise ValidationError(f"Insufficient stock for {prod.name}")

                # atomic decrement
                Product.objects.filter(id=prod.id).update(stock=F('stock') - ci.quantity)

                OrderItem.objects.create(
                    order=order,
                    product=prod,
                    quantity=ci.quantity,
                    price=prod.price,
                    address=user.address
                )
                total += (prod.price * ci.quantity)

            order.total_price = total
            order.save()
            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
