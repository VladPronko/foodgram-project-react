from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import RecipeSubscriptionSerializer

from .models import Favourites, Ingredient, Recipe, Tag
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeSerializer,
                          TagsSerializer)


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

    @action(detail=False, methods=["POST", "DELETE"], url_path=r'(?P<id>\d+)/favorite',
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        serializer = FavoriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        if request.method == "POST":
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, recipe=recipe)
            # serializer = ShowFollowsSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(Favourites, user=request.user, recipe__id=id)
        favorite.delete()
        return Response(
            f'Рецепт {favorite.recipe} удален из избранного у пользователя '
            f'{request.user}', status=status.HTTP_204_NO_CONTENT
        )


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
