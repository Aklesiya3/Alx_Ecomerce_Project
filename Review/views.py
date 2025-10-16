from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        # Resolve product instance and pass it to serializer.save
        from Product.models import Product
        product = None
        if product_id is not None:
            product = Product.objects.filter(id=product_id).first()
        serializer.save(user=self.request.user, product=product)