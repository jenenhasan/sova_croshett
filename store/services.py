from .serializers import CheckoutSerializer


class CheckoutService:
    """
    TODO  take validated checkout data + the
    customer's Cart, and turn it into an Order with OrderItems, e.g.:

        def __init__(self, cart, validated_data):
            self.cart = cart
            self.validated_data = validated_data

        def create_order(self):
            # 1. Create Order from validated_data (customer_name, phone, etc.)
            # 2. Loop over cart.items, create OrderItem per CartItem
            #    (snapshot product price into total_price)
            # 3. Sum total_price on the Order
            # 4. Clear the cart
            # 5. Return the created Order
            ...
    """
    pass
