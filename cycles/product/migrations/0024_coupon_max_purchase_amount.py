# Generated by Django 4.2.4 on 2024-01-03 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_remove_coupon_max_purchase_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='max_purchase_amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]