from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .models import Favourites, Ingredient, Recipe, Shopping_cart, Tag
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagsSerializer)


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
            if Favourites.objects.filter(recipe=recipe, user=request.user).exists():
                raise ValidationError('Данный рецепт уже есть в Вашем списке избранных!')
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, recipe=recipe)
            # print(serializer.data)
            # serializer = ShowFollowsSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            favorite = get_object_or_404(Favourites, user=request.user, recipe__id=id)
            favorite.delete()
        return Response(
            f'Рецепт {favorite.recipe} удален из избранного у пользователя '
            f'{request.user}', status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=["POST", "DELETE"], url_path=r'(?P<id>\d+)/shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        serializer = ShoppingCartSerializer(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        if request.method == "POST":
            if Shopping_cart.objects.filter(recipe=recipe, user=request.user).exists():
                raise ValidationError('Вы уже добавили данный рецепт в список покупок!')
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, recipe=recipe)
            # print(serializer.data)
            # serializer = ShowFollowsSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE":
            shopping_cart = get_object_or_404(Shopping_cart, user=request.user, recipe__id=id)
            shopping_cart.delete()
        return Response(
            f'Рецепт {shopping_cart.recipe} удален из списка покупок у пользователя '
            f'{shopping_cart.user}', status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, pk=None):
        shopping_cart = Shopping_cart.objects.filter(user=request.user).all()
        shopping_list = {}
        for item in shopping_cart:
            for recipe_ingredient in item.recipe.recipe_ingredients.all():
                name = recipe_ingredient.ingredients.name
                measuring_unit = recipe_ingredient.ingredients.measurement_unit
                amount = recipe_ingredient.amount
                if name not in shopping_list:
                    shopping_list[name] = {
                        'name': name,
                        'measurement_unit': measuring_unit,
                        'amount': amount
                    }
                else:
                    shopping_list[name]['amount'] += amount
        content = (
            [f'{item["name"]} ({item["measurement_unit"]}) '
            f'- {item["amount"]}\n'
            for item in shopping_list.values()]
        )
        filename = 'shopping_list.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(filename)
        )
        return response


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
