import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.pagination import PageNumberPagination

from .serializers import (RecipeSerializer, TagSerializer, FavoriteSerializer,
                          IngredientSerializer, FavoriteAndCartSerializer,
                          CartSerializer)
from recipes.models import Recipe, Tag, Favorite, Ingredient, Cart
from users.models import User


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['get'], detail=False,
            url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def download_shopping_cart(self, request, *args, **kwargs):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        user = get_object_or_404(User, id=request.user.id)
        all_carts = Cart.objects.filter(user=user).all()
        ingredients = dict()
        for cart in all_carts:
            for ingredient in list(cart.recipe.related_ingredient.all()):
                if ingredient.ingredient not in ingredients:
                    ingredients[ingredient.ingredient] = ingredient.value
                else:
                    ingredients[ingredient.ingredient] += ingredient.value
        list_of_ingredients = ''
        for key, value in ingredients.items():
            list_of_ingredients += f'\n{key}: {value}'
        p.drawRightString(200, 200, list_of_ingredients)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Список покупок.pdf')
    
    @action(methods=['get', 'delete'], detail=False,
            url_path=r'(?P<id>\d+)/favorite')
    def favorite(self, request, id=None, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        if request.method == 'GET':
            favorite_serializer = FavoriteSerializer(data={'user': user.id, 'recipe': recipe.id})
            favorite_serializer.is_valid(raise_exception=True)
            favorite_serializer.save()
            serializer = FavoriteAndCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', 'delete'], detail=False,
            url_path=r'(?P<id>\d+)/shopping_cart')
    def shopping_cart(self, request, id=None, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        if request.method == 'GET':
            shop_serializer = CartSerializer(data={'user': user.id, 'recipe': recipe.id})
            shop_serializer.is_valid(raise_exception=True)
            shop_serializer.save()
            serializer = FavoriteAndCartSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            cart = get_object_or_404(Cart, user=user, recipe=recipe)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ['get']


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    http_method_names = ['get']
