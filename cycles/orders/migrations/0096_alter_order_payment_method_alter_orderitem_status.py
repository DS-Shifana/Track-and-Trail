# Generated by Django 4.2.4 on 2024-01-04 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0095_alter_order_payment_method_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Razorpay', 'Razorpay'), ('Wallet', 'Wallet'), ('Cash On Delivery', 'Cash On Delivery')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Out For Shipping', 'Out For Shipping'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]
