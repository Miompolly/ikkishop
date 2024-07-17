from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse

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

