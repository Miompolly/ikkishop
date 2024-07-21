# orders/forms.py

from django import forms
from .models import Payment
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['first_name', 'last_name', 'email', 'phone','district', 'sector', 'cell','total_price','tax','amount']


