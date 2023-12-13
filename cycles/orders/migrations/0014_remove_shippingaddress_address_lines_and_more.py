# Generated by Django 4.2.6 on 2023-11-13 06:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0013_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='address_lines',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='mobile',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='address',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='email',
            field=models.EmailField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Out For Shipping', 'Out For Shipping')], default='Pending', max_length=150),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='state',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
