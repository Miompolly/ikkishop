from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest,request
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from .models import Product
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')

    try:
        paged_products = paginator.page(page_number)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)

    context = {
        'products': paged_products,
        'product_count': paginator.count,
    }

    return render(request, 'store/store.html', context)
def product_detail(request, category_slug, product_slug):

    try:

        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    except Exception as e:
        raise e

    context={
        'single_product':single_product,
        'in_cart':in_cart,
    }   
    return render(request, 'store/product_detail.html',context)