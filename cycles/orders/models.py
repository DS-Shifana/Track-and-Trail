from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from product.models import Coupon, Product, ProductVarient

    
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,null=False)
    address= models.TextField(max_length=150,null=False)
    city = models.CharField(max_length=150,null=False)
    state = models.CharField(max_length=150,null=False)
    country = models.CharField(max_length=150,null=False)
    pincode = models.CharField(max_length=10,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username    
    

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    first_name = models.CharField(max_length=150,null=True,blank=True)
    last_name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(max_length=150,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)
    address= models.TextField(max_length=150,null=True,blank=True)
    city = models.CharField(max_length=150,null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    country = models.CharField(max_length=150,null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    status = models.BooleanField(default=False)
    def _str_(self):
        return self.username   

 
    
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress,null=True, blank=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(max_digits=10, decimal_places=2) 
    is_ordered = models.BooleanField(default=False)
    tracking_no = models.CharField(max_length=150,null=True)
    PAYMENT_METHODS = {
            ('Cash On Delivery', 'Cash On Delivery'),
            ('Razorpay', 'Razorpay'),
            ('Wallet','Wallet')
            }
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS, default='Cash On Delivery')
    razor_pay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=255, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    applied_coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no) 
     
    @property
    def total_amount(self):
        order_items = self.orderitem_set.all()
        amount = 0
        for order_item in order_items:
            amount += order_item.price

        if self.applied_coupon:
           if amount >= self.applied_coupon.min_purchase_amount:
               return amount - self.applied_coupon.discount_amount    

        # Ensure the total amount is at least 1 INR
        amount = max(amount, 1.00)
    
        return amount
    

    
    
class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    brake = models.ForeignKey(ProductVarient,on_delete=models.SET_NULL,null=True,blank=True)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    orderstatuses={
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    }
    status = models.CharField(max_length=150,choices=orderstatuses,default='Pending')



    def __str__(self):
        return'{} {}'.format(self.order.id, self.order.tracking_no) 

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    amount = models.FloatField(null=True,blank=True,default=0) 
    referral_code = models.CharField(max_length=50,blank=True,null=True)  

    def __str__(self):
        return str(self.user)  

