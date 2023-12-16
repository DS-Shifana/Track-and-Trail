# Generated by Django 4.2.6 on 2023-11-17 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('PayPal', 'PayPal'), ('Cash On Delivery', 'Cash On Delivery')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Out For Shipping', 'Out For Shipping')], default='Pending', max_length=150),
        ),
    ]