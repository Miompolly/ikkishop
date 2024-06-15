from django.shortcuts import render, redirect

def register(request):
    # Your registration logic here
    return render(request, 'accounts/register.html')

def login(request):
    # Your login logic here
    return render(request, 'accounts/login.html')

def logout(request):
    # Your logout logic here
    return redirect('accounts/login')
