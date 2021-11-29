from rest_framework import serializers

from recipes.models import (Ingredient, Recipe, IngredientRecipe,
                            Tag, Follow, FavoriteRecipe)


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = FavoriteRecipe


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Follow


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient

'''
class CartSerializer(serializers.ModelSerializer):
    pass
'''
