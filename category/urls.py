# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('add/', views.add_category, name='add_category'),
    path('<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/edit/', views.edit_category, name='edit_category'),
]
