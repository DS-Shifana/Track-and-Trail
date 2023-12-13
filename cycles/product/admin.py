from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category) 
admin.site.register(ProductImage)
admin.site.register(ProductVarient)
admin.site.register(Coupon)





