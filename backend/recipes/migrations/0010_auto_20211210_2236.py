# Generated by Django 3.2.7 on 2021-12-11 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_rename_unit_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
    ]
