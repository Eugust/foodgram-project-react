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
                          FollowSerializer, IngredientSerializer, FavoriteAndCartSerializer,
                          CartSerializer)
from recipes.models import Recipe, Tag, Favorite, Follow, Ingredient, Cart
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
        #p.drawString(100, 100, "Hello world.")
        user = get_object_or_404(User, id=request.user.id)
        cart = Cart.objects.filter(user=user).all()
        list_of_ingredients = ''
        for recipe in cart:
            print(recipe.recipe.related_ingredient.name)
            list_of_ingredients += f'{recipe.recipe.title}'
        p.drawRightString(100, 100, f'{list_of_ingredients}')
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
    http_method_names = ['get']


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'delete']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        following = Follow.objects.filter(user=user).all()
        return following


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ['get']
