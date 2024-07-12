from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('category/',views.category,name='category'),
    path('add_category/',views.add_category,name='add_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),    
    path('category/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:category_id>/update/', views.update_category, name='update_category'),


]
