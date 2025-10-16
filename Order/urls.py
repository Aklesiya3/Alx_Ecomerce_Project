from django.urls import path
from .views import CreateOrderView, OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', CreateOrderView.as_view(), name='order-create'),
]