# Generated by Django 3.2.7 on 2021-12-09 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20211208_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='users_add_to_cart',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='users_add_to_favorite',
        ),
    ]