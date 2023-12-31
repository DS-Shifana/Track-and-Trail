# Generated by Django 4.2.4 on 2023-12-28 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0076_alter_order_payment_method_alter_orderitem_status'),
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
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Shipped', 'Shipped'), ('Out For Shipping', 'Out For Shipping'), ('Pending', 'Pending'), ('Delivered', 'Delivered')], default='Pending', max_length=150),
        ),
    ]
