# Generated by Django 4.2.4 on 2024-01-05 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0097_alter_order_payment_method_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('Wallet', 'Wallet'), ('Razorpay', 'Razorpay')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Out For Shipping', 'Out For Shipping'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]
