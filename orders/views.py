from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Payment 
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
        payment = Payment(
            user=request.user,  
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            district=district,
            sector=sector,
            cell=cell,            
            total_price=total_price,
            tax=tax,
            amount=total_amount,
        )
        payment.save()

        
        cart_items.delete()  
        return redirect(reverse('store'))  
    return render(request, 'store/cart.html')
