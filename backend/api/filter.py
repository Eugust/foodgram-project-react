from django_filters import rest_framework as filters

from users.models import User
from recipes.models import Recipe, Ingredient


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name', )
