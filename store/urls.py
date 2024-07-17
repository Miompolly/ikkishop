from django.urls import path
from . import views

urlpatterns = [    
    path('', views.store,name='store'),
    path('category/<slug:category_slug>/', views.store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),   
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product_list/', views.product_list, name='product_list'),
]
