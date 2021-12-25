# Generated by Django 3.2.7 on 2021-12-24 02:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0013_alter_recipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='users_in_favorite',
            field=models.ManyToManyField(related_name='users_in_favorite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recipe',
            name='users_in_shopping_cart',
            field=models.ManyToManyField(related_name='users_in_shopping_cart', to=settings.AUTH_USER_MODEL),
        ),
    ]