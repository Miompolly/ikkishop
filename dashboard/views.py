from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView
from django.contrib import messages
from orders.models import Order, OrderProduct
from store.models import Product
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import UserForm, UserProfileForm
from accounts.models import UserProfile
from orders.models import Order, OrderProduct
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from orders.models import Order, OrderProduct



@login_required(login_url='login')
def category(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/store.html', {'categories': categories})

@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('category')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form})

@login_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category')
    return render(request, 'dashboard/confirm_delete.html', {'category': category})

@login_required(login_url='login')
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'dashboard/edit_category.html', {'category': category})

@login_required(login_url='login')
def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category')
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/edit_category.html', {'form': form, 'category': category})

@login_required(login_url='login')
def dashboard_order(request):
    user = request.user
    order_products = OrderProduct.objects.filter(product__user=user)
    orders = Order.objects.filter(orderproduct__in=order_products).distinct()
    return render(request, 'dashboard/order.html', {'orders': orders, 'order_products': order_products})

class OrderDetailView(DetailView):
    model = Order
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs['id'])

@login_required(login_url='login')
def seller_dashboard(request):
    user = request.user

    user_products = Product.objects.filter(user=user)
    user_order_products = OrderProduct.objects.filter(product__in=user_products)
    user_orders = Order.objects.filter(orderproduct__in=user_order_products).distinct()

    total_orders = user_orders.count()
    completed_orders = user_orders.filter(status='completed').count()
    cancelled_orders = user_orders.filter(status='canceled').count()
    shipped_orders = user_orders.filter(status='shipped').count()
    new_orders = user_orders.filter(status='pending').count()
    recent_orders = user_orders.order_by('-created_at')[:10]

    context = {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'shipped_orders': shipped_orders,
        'new_orders': new_orders,
        'recent_orders': recent_orders,
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='login')
def editprofile(request):
    user = request.user
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('seller_dashboard')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/editprofile.html', context)


