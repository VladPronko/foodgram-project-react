from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from users.serializers import CustomUserSerializer

from .models import Ingredient, Recipe, Tag


class TagsSerializer(ModelSerializer):
    """Сериализатор тега."""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(ModelSerializer):
    """Сериализатор ингридиентов."""
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeSerializer(ModelSerializer):
    """Сериализатор для создания рецепта."""
    author = CustomUserSerializer(read_only=True)
    ingredients = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        many=True
        )
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
        )

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        recipe.save()
        return recipe


class RecipeReadSerializer(ModelSerializer):
    """Сериализатор для просмотра рецепта."""
    author = CustomUserSerializer(read_only=True)
    tags = TagsSerializer(many=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        ]
