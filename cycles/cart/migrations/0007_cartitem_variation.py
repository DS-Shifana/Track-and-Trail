# Generated by Django 4.2.6 on 2023-11-28 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_remove_product_price_product_varient_price'),
        ('cart', '0006_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='product.product_varient'),
        ),
    ]