from django.contrib import admin
from .models import Payment,Order,OrderProduct

admin.site.register(Payment)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'order_total', 'status', 'is_ordered')
    list_filter = ('status', 'is_ordered')
    search_fields = ('order_number', 'user__username', 'email')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order','user', 'product', 'quantity', 'product_price','ordered')
