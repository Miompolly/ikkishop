from django.urls import path
from . import views


urlpatterns = [
    path('seller_dashboard',views.seller_dashboard,name='seller_dashboard'),
    path('category/',views.category,name='category'),
    path('add_category/',views.add_category,name='add_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),    
    path('category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/<int:category_id>/update/', views.update_category, name='update_category'),
    path('order/', views.dashboard_order, name='dashboard_order'),    
    path('order/<int:id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('edit_profile/', views.editprofile, name='editprofile'),
   
]
