from datetime import date
from django.utils import timezone
from django import forms
from .models import  ProductVarient, Offers
from .models import Coupon
from django.core.exceptions import ValidationError



class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVarient
        fields = ['brake', 'price','stock_quantity']



class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'valid_upto', 'discount_amount', 'min_purchase_amount', 'max_purchase_amount', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        valid_upto = cleaned_data.get('valid_upto')
        
        # Add any additional validation logic here

        return cleaned_data
    
class OffersForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ['name', 'start_date', 'end_date', 'percentage', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise ValidationError("End date must be greater than the start date.")

        if start_date and start_date < timezone.now():
            raise ValidationError("Start date must be in the future.")

        return cleaned_data



