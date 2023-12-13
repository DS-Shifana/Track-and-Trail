from .models import Order, ShippingAddress
from django import forms
from django.contrib.auth.models import User
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'shipping_address', 'payment_method'
        ]
        widgets = {
            'shipping_address' : forms.RadioSelect(),
            'payment_method': forms.RadioSelect(),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['user', 'first_name','last_name','email','phone','address','city','state','country','pincode', 'status']
