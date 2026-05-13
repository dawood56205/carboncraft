from django import forms
from products.models import products
from services.models import Service

class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = '__all__' # This pulls every field from your old Product model

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__' # Pulls name, price, duration, etc., from your model

