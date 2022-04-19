from rest_framework import viewsets

from .models import Ingredient, Recipe, Tag
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeSerializer, TagsSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        """
        Данный метод нужен, так как при создании
        и просмотре рецепта необходимы разные поля (сериализаторы).
        """
        if self.request.method in ['GET']:
            return RecipeReadSerializer
        return RecipeSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
