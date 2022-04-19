from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)
from users.serializers import CustomUserSerializer

from .models import Ingredient, IngredientsForRecipes, Recipe, Tag


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientRecipeSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredients.id')
    name = ReadOnlyField(source='ingredients.name')
    measurement_unit = ReadOnlyField(source='ingredients.measurement_unit')

    class Meta:
        model = IngredientsForRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    image = Base64ImageField(max_length=None, use_url=True)
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

    def get_ingredients(self, obj):
        objects = IngredientsForRecipes.objects.filter(recipe=obj)
        serializer = IngredientRecipeSerializer(objects, many=True)
        return serializer.data

    def create(self, validated_data):
        print(validated_data)
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        ingredients_set = request.data['ingredients']
        for ingredient in ingredients_set:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            IngredientsForRecipes.objects.create(
                recipe=recipe,
                ingredients=ingredient_model,
                amount=ingredient['amount']
            )
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        recipe = instance
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
            )
        instance.save()
        instance.tags.set(tags)
        IngredientsForRecipes.objects.filter(recipe=instance).delete()
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            ingredient_model = Ingredient.objects.get(id=ingredient.get('id'))
            IngredientsForRecipes.objects.create(
                recipe=recipe,
                ingredients=ingredient_model,
                amount=ingredient.get('amount')
                )
        return instance


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
