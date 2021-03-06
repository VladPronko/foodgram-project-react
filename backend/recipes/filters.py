from enum import Enum
from django_filters import rest_framework as filters
from django_filters.filters import (AllValuesMultipleFilter,
                                    NumberFilter)
from .models import Recipe


class IsFavorited(Enum):
    IN = 1
    NOT_IN = 0


class IsInCart(Enum):
    IN = 1
    NOT_IN = 0


class RecipeFilter(filters.FilterSet):
    """
    Данный кастомный фильтр необходим нам для возможности фильтрации
    по 'вычисляемым на ходу полям': 'is_favorited' и 'is_in_shopping_cart'.
    """
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = NumberFilter(method='get_is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == IsFavorited.IN.value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == IsInCart.IN.value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
