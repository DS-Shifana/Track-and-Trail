# Generated by Django 4.2.4 on 2024-01-04 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0090_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Wallet', 'Wallet'), ('Cash On Delivery', 'Cash On Delivery'), ('Razorpay', 'Razorpay')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping')], default='Pending', max_length=150),
        ),
    ]
