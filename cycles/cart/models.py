from django.db import models
from product.models import Product,ProductVarient
from django.utils import timezone
from django.contrib.auth.models import User



# Create your models here.
class Cart(models.Model):
       
    cart_id = models.CharField(max_length=250,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True ,blank=True)
    date_added = models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
        return str(self.user) if self.cart_id else self.user.email
    
    def total_amount(self):
            cart_items = self.CartItem.all() 
            for cart_item in cart_items:
                amount += cart_item.product.price * cart_item.quantity
            return amount
    
    
class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVarient, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)        
    quantity = models.IntegerField(default=1)
    date_item_added = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        if self.product and self.product.offer:
            price = self.discount_amount()
        else:
            price = float(self.variation.price)
        
        return price * float(self.quantity)

    
    def discount_amount(self):
        if self.product.offer:
            return float(float(self.variation.price) - (float(self.variation.price) * (self.product.offer.percentage / 100)))
        return 0.0


    def __str__(self):
        return str(self.product)
    