# Generated by Django 3.2.7 on 2021-12-08 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20211207_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoriterecipe',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='favoriterecipe',
            name='recipe',
        ),
        migrations.AddField(
            model_name='cart',
            name='is_in_shopping_cart',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='favorite',
            name='is_favorited',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='cart',
            name='recipe',
        ),
        migrations.AddField(
            model_name='cart',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='recipe',
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CartRecipe',
        ),
        migrations.DeleteModel(
            name='FavoriteRecipe',
        ),
    ]
