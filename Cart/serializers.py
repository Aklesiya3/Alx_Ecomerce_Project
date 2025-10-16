from rest_framework import serializers
from .models import CartItem
from Product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'added_at']

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data.pop('product_id')
        quantity = validated_data.get('quantity', 1)
        obj, created = CartItem.objects.get_or_create(user=user, product_id=product_id, defaults={'quantity': quantity})
        if not created:
            obj.quantity = obj.quantity + quantity
            obj.save()
        return obj