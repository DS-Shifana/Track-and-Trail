# Generated by Django 4.2.6 on 2023-10-18 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cycle_store', '0004_remove_product_length_remove_product_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
