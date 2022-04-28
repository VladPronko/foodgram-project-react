from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        SerializerMethodField, ValidationError)

from recipes.models import Recipe

from .models import Follow

User = get_user_model()


class CustomUserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class RecipeSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShowFollowsSerializer(CustomUserSerializer):
    recipes = SerializerMethodField()
    recipes_count = IntegerField(source='recipes.count')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        return RecipeSubscriptionSerializer(recipes, many=True).data


class FollowSerializer(ModelSerializer):
    user = IntegerField(source='user.id')
    author = IntegerField(source='author.id')

    class Meta:
        model = Follow
        fields = ('user', 'author')

    def validate(self, data):
        user = data['user']['id']
        author = data['author']['id']
        follow_exist = Follow.objects.filter(
            user=user, author__id=author
        ).exists()
        if user == author:
            raise ValidationError(
                'Вы не можете подписаться на самого себя!'
            )
        if follow_exist:
            raise ValidationError('Вы уже подписаны на этого автора!')
        return data

    def create(self, validated_data):
        author = validated_data.get('author')
        author = get_object_or_404(User, pk=author.get('id'))
        user = validated_data.get('user')
        return Follow.objects.create(user=user, author=author)
