from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (RecipeViewSet, TagViewSet,
                    FollowViewSet, IngredientViewSet)
from users.views import UserViewSet, login

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
'''
router.register(
    r'users/subscriptions',
    FollowViewSet,
    basename='follow'
)
'''
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
    path('', include(router.urls)),
]
