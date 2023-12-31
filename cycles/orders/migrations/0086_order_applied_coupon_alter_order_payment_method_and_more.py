# Generated by Django 4.2.4 on 2024-01-03 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_remove_coupon_max_purchase_amount'),
        ('orders', '0085_remove_order_applied_coupon_alter_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='applied_coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.coupon'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Razorpay', 'Razorpay'), ('Cash On Delivery', 'Cash On Delivery'), ('Wallet', 'Wallet')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Out For Shipping', 'Out For Shipping'), ('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
    ]
