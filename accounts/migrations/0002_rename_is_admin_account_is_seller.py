# Generated by Django 5.0.7 on 2024-07-24 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_admin',
            new_name='is_seller',
        ),
    ]
