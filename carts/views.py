from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem, Product

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()
        cart_id = request.session.session_key
    return cart_id

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
    
    # Redirect to cart page after adding item
    return redirect('cart')

def cart(request):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
    total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    quantity = sum(cart_item.quantity for cart_item in cart_items)
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    
    return render(request, 'store/cart.html', context)
