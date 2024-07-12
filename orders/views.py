import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Order
from carts.models import CartItem

@login_required
def place_order(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        district = request.POST.get('district')
        sector = request.POST.get('sector')
        cell = request.POST.get('cell')

        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.sub_total for item in cart_items)
        tax = 0.1 * total_price
        total_amount = total_price + tax

        # Create the order
        order = Order(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            district=district,
            sector=sector,
            cell=cell,
            order_total=total_amount,
            tax=tax,
            ip=request.META.get('REMOTE_ADDR'),
            is_ordered=True
        )
        order.save()

       
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(order.id)
        order.order_number = order_number
        order.save()

        
        cart_items.delete()

        return redirect(reverse('store'))

    return render(request, 'store/cart.html')
