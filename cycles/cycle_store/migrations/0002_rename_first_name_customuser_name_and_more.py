# Generated by Django 4.2.6 on 2023-10-13 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cycle_store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
    ]