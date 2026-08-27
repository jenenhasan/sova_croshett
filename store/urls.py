from django.urls import path
from .views import (
    ProductListView,
    ProductDetailsView,
    CartView,
    CartItemView,
    OrderDetailView,
    CheckoutView,
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product-details'),

    path('cart/', CartView.as_view(), name='get-cart'),
    path('cart/items/', CartItemView.as_view(), name='add-to-cart'),
    path('cart/items/<int:pk>/', CartItemView.as_view(), name='update-cart'),

    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
