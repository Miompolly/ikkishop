import datetime
from django.contrib import messages
import random
import string
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from store.models import Product
from .models import Order, OrderProduct
from carts.models import CartItem,Cart

def payments(request):
    return render(request, 'orders/payment.html')
    

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
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Retrieve cart items from session
        cart = get_object_or_404(Cart)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
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
            order_number=order_number,
            is_ordered=False  
        )
        order.save()

        # Clear the cart session
        request.session['cart'] = {}

        # Pass context to the template
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': grand_total,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = new_status
        order.save()
        return redirect('order_success', order_id=order.id)
    
def order_success(request):
    return render(request, 'orders/order_success.html')