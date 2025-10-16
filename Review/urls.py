from django.urls import path
from .views import ReviewListCreateView

urlpatterns = [
    path('product/<int:product_id>/', ReviewListCreateView.as_view(), name='product-reviews'),
]