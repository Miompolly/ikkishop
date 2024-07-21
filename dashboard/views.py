from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView


from orders.models import Order, OrderProduct
from store.models import Product
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def seller_dashboard(request):
    return render(request, 'dashboard/dashboard.html')
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
            return redirect('category')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form})

@login_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
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
            return redirect('category')
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/edit_category.html', {'form': form, 'category': category})

@login_required(login_url='login')
def dashboard_order(request):
    user = request.user    
    # Get all OrderProduct instances where the product's user is the logged-in user
    order_products = OrderProduct.objects.filter(product__user=user)    
    # Extract distinct orders from the filtered order products
    orders = Order.objects.filter(orderproduct__in=order_products).distinct()
    return render(request, 'dashboard/order.html',{'orders': orders, 'order_products': order_products})

class OrderDetailView(DetailView):
    model = Order
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs['id'])
    

