# Generated by Django 4.2.6 on 2023-11-28 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_cartitem_variation'),
        ('product', '0014_remove_product_price_product_varient_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='product_varient',
            new_name='ProductVarient',
        ),
    ]
