# Generated by Django 4.2.6 on 2023-11-15 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_remove_shippingaddress_address_lines_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Pending', 'Pending'), ('Out For Shipping', 'Out For Shipping'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered')], default='Pending', max_length=150),
        ),
    ]
