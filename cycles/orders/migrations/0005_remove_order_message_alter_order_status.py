# Generated by Django 4.2.6 on 2023-11-12 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_address_line_1_order_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='message',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Out For Shipping', 'Out For Shipping'), ('Shipped', 'Shipped')], default='Pending', max_length=150),
        ),
    ]