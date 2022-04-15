from django.contrib import admin

from .models import Ingredient, Recipe, Tag


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
