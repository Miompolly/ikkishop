from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    # path('order_success/', views.order_success, name='order_success'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    # path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('order-success/', views.order_success, name='order_success'),
    path('order-cancel/', views.order_cancel, name='order_cancel'),
]
