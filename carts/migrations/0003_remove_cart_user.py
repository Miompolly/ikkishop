# Generated by Django 5.0.7 on 2024-07-20 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
    ]
