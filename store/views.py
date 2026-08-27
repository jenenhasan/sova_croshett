from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ProductSerializers,
    CartItemSerializers,
    CartSerializers,
    OrderSerializer,
    OrderItemSerializer,
    CheckoutSerializer,
)
from .models import Product, Cart, CartItem, Order
from .services import CheckoutService


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_available=True)
        # many=True: serialize a collection of products.
        # Without it, DRF would expect a single product instance.
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)


class ProductDetailsView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializers(product)
        return Response(serializer.data)


class CartView(APIView):
    """GET /api/cart/ - return the current customer's cart."""

    def get(self, request):
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        cart, created = Cart.objects.get_or_create(session_id=session_id)
        serializer = CartSerializers(cart)
        return Response(serializer.data)


class CartItemView(APIView):
    """Add / update / remove an item in the cart."""

    def post(self, request):
        """POST /api/cart/items/ - add a product to the cart."""
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        product_id = request.data.get('product')
        quantity = request.data.get('quantity')

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {"error": "Quantity must be greater than 0"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (TypeError, ValueError):
            return Response(
                {"error": "Quantity must be a valid number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found or unavailable"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart, created = Cart.objects.get_or_create(session_id=session_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializers(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        """PATCH /api/cart/items/{id}/ - update an item's quantity."""
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        cart = get_object_or_404(Cart, session_id=session_id)

        quantity = request.data.get('quantity')
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response(
                    {"error": "Quantity must be greater than 0"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (TypeError, ValueError):
            return Response(
                {"error": "Quantity must be a valid number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializers(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """DELETE /api/cart/items/{id}/ - remove an item from the cart."""
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        cart = get_object_or_404(Cart, session_id=session_id)
        cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
        cart_item.delete()

        serializer = CartSerializers(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    def get(self, request, pk):
        """GET /api/orders/{id}/"""
        order = get_object_or_404(Order, id=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class CheckoutView(APIView):
    def post(self, request):
        """POST /api/checkout/"""
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      #still have to add the checkout service 
        return Response(
            {'message': 'Checkout data is valid'},
            status=status.HTTP_200_OK
        )
