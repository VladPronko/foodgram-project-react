from django.contrib import admin

from .models import Ingredient, IngredientsForRecipes, Recipe, Tag


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

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'text',
        'cooking_time'
    )

@admin.register(IngredientsForRecipes)
class IngredientsForRecipesAdmin(admin.ModelAdmin):
    """Настраиваем управление ингридиентами для рецепта через панель
        администратора Джанго."""
    list_display = ('id', 'ingredients', 'recipe', 'amount')
