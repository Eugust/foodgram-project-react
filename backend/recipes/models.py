from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from colorfield.fields import ColorField

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'
        ordering = ['name']

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


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
        ordering = ('id', )

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
    name = models.CharField(max_length=256)
    image = models.ImageField(
        upload_to='media/',
        null=True,
        blank=True
    )
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    users_in_favorite = models.ManyToManyField(
        User,
        related_name='users_in_favorite',
        verbose_name='У пользователей в избранном',
        blank=True
    )
    users_in_shopping_cart = models.ManyToManyField(
        User,
        related_name='users_in_shopping_cart',
        verbose_name='У пользователей в корзине',
        blank=True
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='related_ingredient'
    )
    value = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'ингридиенты для рецепта'
        verbose_name_plural = 'ингридиенты для рецепта'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'список избранных'
        verbose_name_plural = 'список избранных'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def get_list(self):
        total = 0
        for recipe in self.recipe.all():
            total += recipe.related_ingredient.count()
        return total


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
        return '{} subscribe to {}'.format(self.user, self.following)
