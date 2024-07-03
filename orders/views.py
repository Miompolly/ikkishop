# orders/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderItem
from carts.models import CartItem

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            cart_items.delete()

            messages.success(request, 'Your order has been placed successfully.')
            return redirect('store')
    else:
        form = OrderForm()

    context = {'form': form}
    return render(request, 'store/checkout.html', context)
