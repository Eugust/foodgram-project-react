from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Ingredient, Recipe, IngredientRecipe,
                            Tag, Follow, Favorite, User, Cart)
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit'
        )
        model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'recipe')
        model = Favorite

        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe')
            )
        ]


class FavoriteAndCartSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
    
    def get_image(self, obj):
        return obj.image.url
    

class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        queryset=Ingredient.objects.all()
    )
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
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
    ingredients = IngredientRecipeSerializer(
        read_only=True,
        many=True,
        source='related_ingredient'
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
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
            'name',
            'image',
            'text',
            'cooking_time'
        )
    
    def get_is_favorited(self, obj):
        request = self.context['request']
        user = self.context['request'].user
        if request and user.is_authenticated:
            return Favorite.objects.filter(user=user).exists()
        return False
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        user = self.context['request'].user
        if request and user.is_authenticated:
            return Cart.objects.filter(user=user).exists()
        return False


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'following')
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



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'recipe')

        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=('user', 'recipe')
            )
        ]
