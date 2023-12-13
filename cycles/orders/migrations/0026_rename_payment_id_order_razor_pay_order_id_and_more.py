# Generated by Django 4.2.6 on 2023-11-17 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0025_remove_order_payment_status_alter_orderitem_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment_id',
            new_name='razor_pay_order_id',
        ),
        migrations.AddField(
            model_name='order',
            name='razor_pay_payment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razor_pay_payment_signature',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('PayPal', 'PayPal'), ('Cash On Delivery', 'Cash On Delivery')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out For Shipping', 'Out For Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
    ]
