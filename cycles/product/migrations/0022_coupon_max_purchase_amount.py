# Generated by Django 4.2.4 on 2024-01-03 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_alter_productvarient_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='max_purchase_amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
