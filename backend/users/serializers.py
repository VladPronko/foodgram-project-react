from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import CustomUser, Follow

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'imgage', 'cooking_time')


class ShowFollowsSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        # recipes = obj.recipes.all()[:3]
        # return RecipeSubscriptionSerializer(recipes, many=True).data
        return True

    def get_recipes_count(self, obj):
        # queryset = Recipe.objects.filter(author=obj)
        # return queryset.count()
        return True


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    author = serializers.IntegerField(source='author.id')

    class Meta:
        model = Follow
        fields = ['user', 'author']

    def validate(self, data):
        user = data['user']['id']
        author = data['author']['id']
        follow_exist = Follow.objects.filter(
            user=user, author__id=author
        ).exists()
        if user == author:
            raise serializers.ValidationError(
                {"errors": 'Вы не можете подписаться на самого себя'}
            )
        elif follow_exist:
            raise serializers.ValidationError({"errors": 'Вы уже подписаны'})
        return data

    def create(self, validated_data):
        author = validated_data.get('author')
        author = get_object_or_404(User, pk=author.get('id'))
        user = validated_data.get('user')
        return Follow.objects.create(user=user, author=author)
















# class CustomUserSerializer(UserSerializer):
#     """Сериализатор для отображения страницы уже созданного пользователя."""
#     # is_subscribed = SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'id', 'username', 'first_name',
#                   'last_name']
    
#     # def get_is_subscribed(self, obj):
#     #     """Здесь логика расчета поля 'is_subscribed'."""
#     #     return False


# class CustomUserCreateSerializer(UserCreateSerializer):
#     """Сериализатор для страницы создания нового пользователя."""

#     class Meta:
#         model = CustomUser
#         fields = ('email', 'id', 'username', 'first_name',
#                   'last_name', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser(
#             email=validated_data['email'],
#             username=validated_data['username'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
            
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


# class RecipeSubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time')


# class FollowSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='author.email')
#     id = serializers.EmailField(source='author.id')
#     username = serializers.EmailField(source='author.username')
#     first_name = serializers.EmailField(source='author.first_name')
#     last_name = serializers.EmailField(source='author.last_name')
#     is_subscribed = serializers.SerializerMethodField(read_only=True)
#     recipes_count = serializers.SerializerMethodField(read_only=True)
#     recipes = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Follow
#         fields = [
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count'
#         ]

#     def get_is_subscribed(self, obj):
#         user = self.context['request'].user
#         if user.is_anonymous:
#             return False
#         return Follow.objects.filter(
#             user=user, author=obj.author
#         ).exists()

#     def get_recipes_count(self, obj):
#         return obj.author.recipes.count()

#     def get_recipes(self, obj):
#         recipes = obj.author.recipes.all()[:3]
#         return RecipeSubscriptionSerializer(recipes, many=True).data


# class FollowCreateSerializer(ModelSerializer):
#     class Meta:
#         model = Follow
#         fields = ('author', 'user')
