# Generated by Django 4.2.6 on 2023-12-02 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0041_remove_wallet_user_wallet_username_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='username',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Razorpay', 'Razorpay'), ('Cash On Delivery', 'Cash On Delivery')], default='Cash On Delivery', max_length=100),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Out For Shipping', 'Out For Shipping'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=150),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='referrel_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
