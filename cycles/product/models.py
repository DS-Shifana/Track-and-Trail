from django.db import  models

from adminpanel.models import User,Offers
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user_model



class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100,unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = (
        ('s', 'Small'),
        ('sm', 'Medium'),
        ('m', 'Large'),
        ('l', 'Extra Large'),
        ('xl', 'Double Extra Large'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE,null=True,blank=True)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default='s')
    is_availability = models.BooleanField(default=True)
    


    def __str__(self):
        return self.name
    
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to='images/product_images/', blank=True, null=True)

    def __str__(self):
        return self.image.url


class ProductVarient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brake = models.CharField(max_length=50, default='Disc Brake')
    price = models.PositiveIntegerField(default=0)
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.brake
    
    def discounted_price(self):
        if self.product.offer:
            discount = self.price * (self.product.offer / 100 )
            offer_amount = self.price - discount
            return offer_amount

    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_upto = models.DateTimeField()
    discount_amount = models.PositiveIntegerField()
    min_purchase_amount = models.PositiveIntegerField(default=0)
    max_purchase_amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    used_by = models.ManyToManyField(User, blank=True)  # Many-to-many relationship with users who have used the coupon

    def _str_(self):
        return self.code

    def is_user_eligible(self, user):
        """
        Check if a user is eligible to use the coupon.
        """
        return user not in self.used_by.all() 

    def mark_as_used(self, user):
        """
        Mark the coupon as used by a specific user.
        """
        UserModel = get_user_model()

        if isinstance(user, SimpleLazyObject):
            user._setup()  # Ensure the lazy object is fully initialized
            user = user._wrapped

        if not isinstance(user, UserModel):
            user = UserModel.objects.get(pk=user.pk)    

        self.used_by.add(user)
        self.save()  


    