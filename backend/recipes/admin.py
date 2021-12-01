from django.contrib import admin

from .models import (Ingredient, Recipe, IngredientRecipe,
                     Tag, Follow, FavoriteRecipe, Cart)


class RecipeIngredientLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


class FavoriteRecipeLine(admin.TabularInline):
    model = FavoriteRecipe.recipe.through
    extra = 1


class CartLine(admin.TabularInline):
    model = Cart.recipe.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author', 'title', 'tags')
    inlines = (RecipeIngredientLine, RecipeTagLine, )
    exclude = ('tags',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = (FavoriteRecipeLine,)
    exclude = ('recipe',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',  'get_list')
    inlines = (CartLine,)


# admin.site.register(IngredientRecipe)
