from carts.models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}  # Return an empty dictionary if in admin page
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # Retrieve the cart based on cart_id
            cart_items = CartItem.objects.filter(cart=cart)  # Filter cart items by the retrieved cart

            # Calculate the total cart count by summing up quantities of all cart items
            cart_count = sum(cart_item.quantity for cart_item in cart_items)
        
        except Cart.DoesNotExist:
            cart_count = 0  # Set cart_count to 0 if the cart doesn't exist

    return  dict(cart_count=cart_count)  # Return the cart_count as part of a dictionary
