from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Follow, Recipe


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )
    

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user = self.context['request'].user
        if request and user.is_authenticated:
            return Follow.objects.filter(user=user).exists()
        return False


class RecipeShortInfoSerializer(serializers.ModelSerializer):
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



class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )
    recipes_count = serializers.SerializerMethodField(
        read_only=True
    )
    recipes = RecipeShortInfoSerializer(
        read_only=True,
        many=True
    )
    

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context['request']
        user = self.context['request'].user
        if request and user.is_authenticated:
            return Follow.objects.filter(user=user).exists()
        return False

    def get_recipes_count(self, obj):
        user = self.context['request'].user
        follow_obj = get_object_or_404(Follow, user=user)
        author = follow_obj.following
        recipes_count = Recipe.objects.filter(author=author).count()
        return recipes_count

    def get_recipes(self, obj):
        user = self.context['request'].user
        follow_obj = get_object_or_404(Follow, user=user)
        author = follow_obj.following
        recipes = Recipe.objects.filter(author=author).all()
        return recipes



class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True
    )


    class Meta:
        model = User
        fields = (
            'password',
            'email'
        )


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        required=True,
    )
    current_password = serializers.CharField(
        required=True
    )
