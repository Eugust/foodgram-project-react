import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.pagination import PageNumberPagination

from .serializers import (RecipeSerializer, TagSerializer, FavoriteRecipeSerializer,
                          FollowSerializer, IngredientSerializer)
from recipes.models import Recipe, Tag, FavoriteRecipe, Follow, Ingredient
from users.models import User


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['get'], detail=False, url_path='download_shopping_cart', url_name='download_shopping_cart')
    def download_shopping_cart(self, request, *args, **kwargs):
        buffer = io.BytesIO()

        p = canvas.Canvas(buffer)

        p.drawString(100, 100, "Hello world.")

        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    http_method_names = ['get', 'delete']

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)


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
