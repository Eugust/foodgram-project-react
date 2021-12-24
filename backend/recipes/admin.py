from django.contrib import admin

from .models import (Ingredient, Recipe,
                     Tag, Follow, Favorite, Cart)


class RecipeIngredientLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


class RecipeFavoriteLine(admin.TabularInline):
    model = Recipe.users_in_favorite.through
    extra = 1


class RecipeCartLine(admin.TabularInline):
    model = Recipe.users_in_shopping_cart.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientLine, RecipeTagLine, RecipeFavoriteLine, RecipeCartLine, )
    exclude = ('tags', 'users_in_favorite', 'users_in_shopping_cart')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


# admin.site.register(IngredientRecipe)
