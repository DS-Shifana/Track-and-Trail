# Generated by Django 4.2.4 on 2024-01-03 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0087_alter_orderitem_status'),
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
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]