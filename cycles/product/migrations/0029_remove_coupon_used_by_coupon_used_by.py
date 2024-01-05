# Generated by Django 4.2.4 on 2024-01-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0005_offers'),
        ('product', '0028_remove_coupon_used_by_coupon_used_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='used_by',
        ),
        migrations.AddField(
            model_name='coupon',
            name='used_by',
            field=models.ManyToManyField(blank=True, to='adminpanel.user'),
        ),
    ]
