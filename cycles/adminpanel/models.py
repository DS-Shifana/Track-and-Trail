from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_deleted = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=100,unique=True,blank=True,null=True)
User._meta.get_field('groups').remote_field.related_name = 'custom_user_set'
User._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_set_permissions'  

class Offers(models.Model):
    name = models.CharField(max_length=50,unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    percentage = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.name
