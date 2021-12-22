from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (RecipeViewSet, TagViewSet,
                    IngredientViewSet)
from users.views import UserViewSet, login, logout

router = SimpleRouter()
router.register(
    r'tags',
    TagViewSet,
    basename='tags'
)
router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)
router.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredients'
)
router.register(
    r'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('auth/token/login/', login, name='login'),
    path('auth/token/logout/', logout, name='logout'),
    path('', include(router.urls)),
]
