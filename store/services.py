from .serializers import CheckoutSerializer
from django.db import transaction
from .models import Cart , Product , Order , OrderItem
from decimal import Decimal
class CheckoutService:
    @staticmethod
    @transaction.atomic
    
    def checkout(
            session_id, 
            customer_name,
            customer_phone,
            customer_address="",
            notes=""
    ):
        cart = Cart.objects.filter(
            session_id=session_id
        ).first()    # added .first because we dont want the service to automatically create a cart during checkout 

        #check the cart exist 
        if not cart:
            raise ValueError("cart doesnt exist")
        #check cart is not empty 
        cart_items= cart.items.select_related('product').all()
        if not cart_items.exists():
            raise ValueError("cart is empty")
        
        #validate products 
        for cart_item in cart_items:
            product = cart_item.product
            if not product : 
                raise ValueError("product doesnt exist")
            if not product.is_available:
                raise ValueError (
                    f"{product.name} is no longer available"
                )
            
        #calculate total 
        total_price = Decimal("0.00")
        for cart_item in cart_items:
            product = cart_item.product
            item_total = (
                product.price * cart_item.quantity
            )

            total_price +=item_total
        #create order 
        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address, 
            notes=notes,
            total_price=total_price
        )


        #create order item
        for cart_item in cart_items:
            product= cart_item.product
            
            OrderItem.objects.create(
            order=order,
            product=product,
            quantity=cart_item.quantity,
            total_price=(
                product.price * cart_item.quantity
            )
        )
            
        #clear cart
        cart.items.all().delete()

        #return created order 
        return order


    
