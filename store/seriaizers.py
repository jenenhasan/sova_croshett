# Serializers convert Django model instances to/from JSON so the API
# can communicate with the frontend.
from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
        ]


class ProductSerializers(serializers.ModelSerializer):
    # Nested read-only serializer: returns the full category object.
    # Use `source=` instead when you only need one specific field.
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'category',
            'is_available',
        ]


class CartItemSerializers(serializers.ModelSerializer):
    # We expose product_name/price directly instead of nesting the full
    # ProductSerializers, since the cart doesn't need all product details.
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_name',
            'price',
            'quantity',
        ]


class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    # Not nesting ProductSerializers here either - order items only need
    # the product name, not the full product payload.

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'quantity',
            'total_price',
        ]


class OrderSerializer(serializers.ModelSerializer):
    # Comes from the reverse relationship defined on OrderItem.order
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_name',
            'customer_phone',
            'customer_address',
            'status',
            'total_price',
            'items',
            'notes',
            'created_at',
            'updated_at',
        ]


class CheckoutSerializer(serializers.Serializer):
    # Plain Serializer (not ModelSerializer) because the frontend isn't
    # creating an Order directly - it sends checkout info, and the backend
    # uses that info to build the Order itself.
    customer_name = serializers.CharField(max_length=255)
    customer_phone = serializers.CharField(max_length=50)
    customer_address = serializers.CharField()
    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )
