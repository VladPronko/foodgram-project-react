from django.contrib import admin
from django.contrib.admin import ModelAdmin, display

from .models import Favourites, Ingredient, IngredientsForRecipes, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настраиваем управление тегами через панель
        администратора Джанго."""
    list_display = ('id', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настраиваем управление ингридиентами через панель
        администратора Джанго."""
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'text',
        'added_to_favorites'
        
    )
    list_filter = ('name', 'author', 'tags')
    read_only_fields = ('added_to_favorites',)

    @display(description='Общее число добавлений в избранное')
    def added_to_favorites(self, obj):
        return obj.favorites.count()


@admin.register(IngredientsForRecipes)
class IngredientsForRecipesAdmin(admin.ModelAdmin):
    """Настраиваем управление ингридиентами для рецепта через панель
        администратора Джанго."""
    list_display = ('id', 'ingredients', 'recipe', 'amount')
