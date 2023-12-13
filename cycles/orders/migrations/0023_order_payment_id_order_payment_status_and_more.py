# Generated by Django 4.2.6 on 2023-11-17 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_alter_order_payment_method_alter_orderitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
    ]
