from drf_extra_fields.fields import Base64ImageField
from requests import Response
from rest_framework import serializers
from rest_framework.serializers import (ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)
from users.serializers import CustomUserSerializer

from .models import (Favourites, Ingredient, IngredientsForRecipes, Recipe,
                     Shopping_cart, Tag)


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

    def validate(self, data):
        if len(data['tags']) == 0:
            raise serializers.ValidationError(
                'Необходимо добавить минимум 1 тег')
        if len(data['tags']) > len(set(data['tags'])):
            raise serializers.ValidationError(
                'Теги не должны повторяться!')
        id_ingredients = set()
        ingredients = self.initial_data['ingredients']
        for ingredient in ingredients:
            if ingredient['id'] not in id_ingredients:
                id_ingredients.add(ingredient['id'])
            else:
                raise serializers.ValidationError(
                    'Ингредиенты повторяются!'
                )
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        ingredients_set = request.data['ingredients']
        for ingredient in ingredients_set:
            try:
                ingredient_model = Ingredient.objects.get(id=ingredient['id'])
                amount = ingredient['amount']
            except KeyError:
                raise serializers.ValidationError(
                    'Необходимо добавить ингридиенты к рецепту!'
                )
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    'Указан неверный id ингридиента!'
                )
            if amount:
                IngredientsForRecipes.objects.create(
                    recipe=recipe,
                    ingredients=ingredient_model,
                    amount=amount
                )
            else:
                raise serializers.ValidationError(
                    'Amount не может быть равен 0!'
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
        instance.tags.set(tags)
        instance.save()
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

        # ingredients_data = validated_data.pop('ingredients')
        # tags_data = validated_data.pop('tags')
        # recipe = Recipe.objects.filter(id=instance.id)
        # recipe.update(**validated_data)
        # ingredients_instance = [
        #     ingredient for ingredient in instance.ingredients.all()
        # ]
        # for item in ingredients_data:
        #     amount = item['amount']
        #     ingredient_id = item['id']
        #     if IngredientForRecipe.objects.filter(
        #             id=ingredient_id, amount=amount
        #     ).exists():
        #         ingredients_instance.remove(
        #             IngredientForRecipe.objects.get(id=ingredient_id,
        #                                             amount=amount
        #                                             ).ingredient)
        #     else:
        #         IngredientForRecipe.objects.get_or_create(
        #             recipe=instance,
        #             ingredient=get_object_or_404(Ingredient, id=ingredient_id),
        #             amount=amount
        #         )
        # if validated_data.get('image') is not None:
        #     instance.image = validated_data.get('image', instance.image)
        # instance.ingredients.remove(*ingredients_instance)
        # instance.tags.set(tags_data)
        # return instance


class RecipeReadSerializer(RecipeSerializer):
    """Сериализатор для просмотра рецепта."""
    author = CustomUserSerializer(read_only=True)
    tags = TagsSerializer(many=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        objects = IngredientsForRecipes.objects.filter(recipe=obj)
        serializer = IngredientRecipeSerializer(objects, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.favorites.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        # request = self.context.get('request')
        # if request is None or request.user.is_anonymous:
        #     return False
        # return Shopping_cart.objects.filter(user=request.user, author=obj).exists()
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.shopping_cart.filter(recipe=obj).exists()
        )

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
            'is_favorited', 'is_in_shopping_cart'
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favourites
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Shopping_cart
        fields = ('id', 'name', 'image', 'cooking_time')

    # def validate(self, data):
    #     recipe = data['recipe']
    #     user = data['user']
    #     if user == recipe.author:
    #         raise serializers.ValidationError('You are the author!')
    #     if (Favourites.objects.filter(recipe=recipe, user=user).exists()):
    #         raise serializers.ValidationError('You have already subscribed!')
    #     return data
