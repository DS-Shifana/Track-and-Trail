# Generated by Django 4.2.6 on 2023-12-04 05:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0043_alter_order_payment_method_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Wallet', 'Wallet'), ('Razorpay', 'Razorpay'), ('Cash On Delivery', 'Cash On Delivery')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('valid_upto', models.DateTimeField()),
                ('discount_amount', models.PositiveIntegerField()),
                ('min_purchase_amount', models.PositiveIntegerField(default=0)),
                ('max_purchase_amount', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('used_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
