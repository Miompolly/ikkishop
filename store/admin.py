# store/admin.py
from django.contrib import admin
from .models import Product
from dashboard.models import Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available','category')
    list_filter = ('category', 'is_available')

admin.site.register(Product, ProductAdmin)
