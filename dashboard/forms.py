from django import forms
from dashboard.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryname','description', 'image']


