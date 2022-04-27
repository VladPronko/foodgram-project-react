from django_filters import rest_framework as filters
from django_filters.rest_framework import AllValuesMultipleFilter


class RecipeFilter(filters.FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        field_name='favorites'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
