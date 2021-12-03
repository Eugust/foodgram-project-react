from django.db import models
from django.contrib.auth import get_user_model

from colorfield.fields import ColorField


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    unit = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'
        ordering = ['-name']

    def __str__(self):
        return '{}, {}'.format(self.name, self.unit)


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Введите наименование тега'
    )
    color = ColorField(default='#FF0000')
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text='Укажите адрес для страницы'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ('-id', )

    def __str__(self) -> str:
        return '{}'.format(self.name)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    title = models.CharField(max_length=256)
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank = True
    )
    description = models.TextField()
    cooking_time = models.PositiveIntegerField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes'
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'ингридиенты для рецепта'
        verbose_name_plural = 'ингридиенты для рецепта'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='favorite'
    )

    class Meta:
        verbose_name = 'список избранных'
        verbose_name_plural = 'список избранных'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return '{} подписался на {}'.format(self.user, self.following)


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='cart'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def get_list(self):
        return self.recipe.count()

