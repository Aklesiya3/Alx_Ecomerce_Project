from django.urls import path
from .views import CartListCreateView, CartItemDestroyView

urlpatterns = [
    path('', CartListCreateView.as_view(), name='cart-list-create'),
    path('<int:pk>/', CartItemDestroyView.as_view(), name='cart-item-delete'),
]