# Generated by Django 3.2.7 on 2021-12-24 18:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0016_auto_20211223_1833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientrecipe',
            old_name='value',
            new_name='amount',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='users_in_favorite',
            field=models.ManyToManyField(blank=True, related_name='users_in_favorite', to=settings.AUTH_USER_MODEL, verbose_name='У пользователей в избранном'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='users_in_shopping_cart',
            field=models.ManyToManyField(blank=True, related_name='users_in_shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='У пользователей в корзине'),
        ),
    ]