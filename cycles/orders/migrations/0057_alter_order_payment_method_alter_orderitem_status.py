# Generated by Django 4.2.4 on 2023-12-13 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0056_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Razorpay', 'Razorpay'), ('Cash On Delivery', 'Cash On Delivery'), ('Wallet', 'Wallet')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Pending', 'Pending'), ('Out For Shipping', 'Out For Shipping'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered')], default='Pending', max_length=150),
        ),
    ]
