from django.urls import path
from django.urls import reverse
# from django.contrib import admin
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    # path('admin/', admin.site.urls),
    
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('', views.dashboard, name='dashboard'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),   
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]
