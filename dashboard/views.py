from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Category
from .forms import CategoryForm
# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def category(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/store.html', {'categories': categories})





def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category')
    return render(request, 'dashboard/confirm_delete.html', {'category': category})

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'dashboard/edit_category.html', {'category': category})

def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category')  # Redirect to the category list page
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/edit_category.html', {'form': form, 'category': category})