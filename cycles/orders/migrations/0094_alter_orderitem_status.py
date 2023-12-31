# Generated by Django 4.2.4 on 2024-01-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0093_alter_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]
