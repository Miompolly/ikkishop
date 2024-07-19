import datetime
from django.contrib import messages
import random
import string
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from store.models import Product
from .models import Order, OrderProduct
from carts.models import CartItem

@login_required
def place_order(request):
    if request.method == 'POST':
        # Extracting form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        district = request.POST.get('district')
        sector = request.POST.get('sector')
        cell = request.POST.get('cell')
        grand_total = request.POST.get('grand_total')
        tax = request.POST.get('tax')
        ip = request.META.get('REMOTE_ADDR')

        # Create a new Order
        order = Order(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            district=district,
            sector=sector,
            cell=cell,
            order_total=grand_total,
            tax=tax,
            ip=ip,
            order_number=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        )
        order.save()

        # Process each cart item and create OrderProduct
        cart_items = request.session.get('cart', {})
        for product_id, quantity in cart_items.items():
            product = Product.objects.get(id=product_id)
            order_product = OrderProduct(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            order_product.save()
        # Clear the cart session
        request.session['cart'] = {}

        messages.success(request, "Your order has been placed successfully!")
        return redirect('store')  
    return redirect('store')
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = new_status
        order.save()
        return redirect('order_success', order_id=order.id)
    
def order_success(request):
    return render(request, 'orders/order_success.html')