# Generated by Django 4.2.6 on 2023-10-20 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_is_listed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='availability',
            new_name='is_availability',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_listed',
        ),
    ]
