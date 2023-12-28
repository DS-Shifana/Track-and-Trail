# Generated by Django 4.2.4 on 2023-12-28 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0074_alter_order_payment_method_alter_orderitem_status'),
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
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping')], default='Pending', max_length=150),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='referral_code',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
