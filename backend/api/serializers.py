from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Ingredient, Recipe, IngredientRecipe,
                            Tag, Follow, FavoriteRecipe, User)
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'recipe')
        model = FavoriteRecipe

        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('user', 'recipe')
            )
        ]


class FavoriteAndCartSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'image',
            'cooking_time'
        )
    '''
    def get_image(self, obj):
        return obj.image.url
    '''

class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        queryset=Ingredient.objects.all()
    )
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    unit = serializers.StringRelatedField(
        source='ingredient.unit'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'unit',
            'value'
        )
        model = IngredientRecipe


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        read_only=True,
        many=True
    )
    author = UserSerializer(
        read_only=True
    )
    ingredients = IngredientSerializer(
        read_only=True,
        many=True,
        source='related_ingredient'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'title',
            'image',
            'description',
            'cooking_time'
        )


class FollowSerializer(serializers.ModelSerializer):
    following = UserSerializer(
        read_only=True
    )

    class Meta:
        fields = ('following',)
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Уже подписаны',
            )
        ]

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError(
                "Нельзя подписываться на себя!"
            )
        return data


'''
class CartSerializer(serializers.ModelSerializer):
    pass
'''
