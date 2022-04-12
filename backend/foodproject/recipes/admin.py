from django.contrib import admin

from .models import Ingredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настраиваем управление тегами через панель
        администратора Джанго."""
    list_display = ('name', 'color', 'slug')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Настраиваем управление ингридиентами через панель
        администратора Джанго."""
    list_display = ('name', 'measurement_unit')
