import csv
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, AllowAny,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.pagination import PageNumberPagination
from .serializers import (RecipeSerializer, TagSerializer, FavoriteSerializer,
                          IngredientSerializer, FavoriteAndCartSerializer,
                          CartSerializer, IngredientRecipeSerializer)
from recipes.models import (Recipe, Tag, Favorite,
                            Ingredient, Cart, IngredientRecipe)
from users.models import User


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['get'], detail=False,
            url_path='download_shopping_cart',
            url_name='download_shopping_cart',
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; "filename=shoppinglist.csv"'
            },
        )
        user = get_object_or_404(User, id=request.user.id)
        all_carts = Cart.objects.filter(user=user).all()
        ingredients = dict()
        for cart in all_carts:
            for ingredient in list(cart.recipe.related_ingredient.all()):
                if ingredient.ingredient not in ingredients:
                    ingredients[ingredient.ingredient] = ingredient.value
                else:
                    ingredients[ingredient.ingredient] += ingredient.value

        writer = csv.writer(response)
        for ingredient, amount in ingredients.items():
            writer.writerow([f'{ingredient}', f'{amount}'])
        return response

    @action(methods=['get', 'delete'], detail=False,
            url_path=r'(?P<id>\d+)/favorite',
            permission_classes=[IsAuthenticated])
    def favorite(self, request, id=None, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        if request.method == 'GET':
            favorite_serializer = FavoriteSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            favorite_serializer.is_valid(raise_exception=True)
            favorite_serializer.save()
            serializer = FavoriteAndCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get', 'delete'], detail=False,
            url_path=r'(?P<id>\d+)/shopping_cart',
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        if request.method == 'GET':
            shop_serializer = CartSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            shop_serializer.is_valid(raise_exception=True)
            shop_serializer.save()
            serializer = FavoriteAndCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            cart = get_object_or_404(Cart, user=user, recipe=recipe)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post', 'delete'], detail=False,
            url_path=r'(?P<id>\d+)/add_ingredient',
            permission_classes=[IsAuthenticated])
    def add_ingredient(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        if user == recipe.author:
            if request.method == 'POST':
                serializer = IngredientRecipeSerializer(data=self.request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif request.method == 'DELETE':
                ingredient = get_object_or_404(IngredientRecipe, recipe=recipe)
                ingredient.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return Response(
            status=status.HTTP_423_LOCKED
        )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    http_method_names = ['get']


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    http_method_names = ['get']
