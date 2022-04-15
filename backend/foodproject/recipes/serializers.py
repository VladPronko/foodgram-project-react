from multiprocessing import managers

from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)
from users.serializers import CustomUserSerializer

from .models import Ingredient, IngredientsForRecipes, Recipe, Tag


class TagsSerializer(ModelSerializer):
    """Сериализатор тега."""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(ModelSerializer):
    """Сериализатор ингридиентов."""
    # name = serializers.ReadOnlyField()
    # measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


# class IngredientRecipeSerializer(ModelSerializer):
#     id = PrimaryKeyRelatedField(
#         queryset=Ingredient.objects.all(),
#     )
#     name = serializers.CharField(
#         read_only=True,
#     )
#     measurement_unit = serializers.CharField(
#         read_only=True,
#     )

#     class Meta:
#         model = IngredientsForRecipes
#         fields = ('id', 'name', 'measurement_unit', 'amount')

class IngredientRecipeSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredients.id')
    name = ReadOnlyField(source='ingredients.name')
    measurement_unit = ReadOnlyField(source='ingredients.measurement_unit')

    class Meta:
        model = IngredientsForRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    """Сериализатор для создания рецепта."""
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    # ingredients = IngredientRecipeSerializer(many=True, read_only=True)
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
        # fields = '__all__'

    def get_ingredients(self, obj):
        objects = IngredientsForRecipes.objects.filter(recipe=obj)
        serializer = IngredientRecipeSerializer(objects, many=True)
        return serializer.data

    def create(self, validated_data):
        request = self.context.get('request')
        # ingredients = self.initial_data.get('ingredients')
        # ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        ingredients_set = request.data['ingredients']
        for ingredient in ingredients_set:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            IngredientsForRecipes.objects.create(recipe=recipe, ingredients=ingredient_model, amount=ingredient['amount'])
        recipe.save()
        return recipe


class RecipeReadSerializer(RecipeSerializer):
    """Сериализатор для просмотра рецепта."""
    author = CustomUserSerializer(read_only=True)
    tags = TagsSerializer(many=True)
    ingredients = SerializerMethodField()

    def get_ingredients(self, obj):
        objects = IngredientsForRecipes.objects.filter(recipe=obj)
        serializer = IngredientRecipeSerializer(objects, many=True)
        return serializer.data

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        ]
# class RecipeReadSerializer(RecipeSerializer):
#     """Сериализатор для просмотра рецепта."""
#     tags = TagsSerializer(many=True)
    
