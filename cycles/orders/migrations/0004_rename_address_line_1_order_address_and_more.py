# Generated by Django 4.2.6 on 2023-11-12 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_address_order_address_line_1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address_line_1',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address_line_2',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out For Shipping', 'Out For Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
    ]