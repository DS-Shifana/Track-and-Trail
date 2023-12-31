# Generated by Django 4.2.6 on 2023-12-04 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0002_rename_is_blocked_user_is_deleted'),
        ('product', '0015_rename_product_varient_productvarient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('valid_upto', models.DateTimeField()),
                ('discount_amount', models.PositiveIntegerField()),
                ('min_purchase_amount', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('used_by', models.ManyToManyField(blank=True, to='adminpanel.user')),
            ],
        ),
    ]
