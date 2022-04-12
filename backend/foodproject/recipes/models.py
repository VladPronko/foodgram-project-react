from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (CASCADE, CharField, ForeignKey, ImageField,
                              ManyToManyField, PositiveIntegerField, SlugField,
                              TextField)
from users.models import CustomUser


class Tag(models.Model):
    """Модель тега."""
    name = CharField(verbose_name='Название', max_length=50)
    color = CharField(verbose_name='Цвет в HEX', max_length=10)
    slug = SlugField(verbose_name='Уникальный слаг', max_length=50)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиентов."""
    name = CharField(verbose_name='Название', max_length=200)
    measurement_unit = CharField(
        verbose_name='Единицы измерения',
        max_length=200
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Автор'
        )
    name = CharField(max_length=200, verbose_name='Название')
    image = ImageField(
        verbose_name='Картинка, закодированная в Base64',
        blank=True
        )
    text = TextField(max_length=1000, verbose_name='Описание')
    ingredients = ManyToManyField(
        Ingredient,
        through='IngredientsForRecipes',
        verbose_name='Список ингредиентов'
        )
    tags = ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Список id тегов'
        )
    cooking_time = PositiveIntegerField(
        validators=[MinValueValidator(
            1, 'Минимальное время приготовления - 1 минута')],
        verbose_name='Время приготовления (в минутах)'
        )

    def __str__(self):
        return self.name


class IngredientsForRecipes(models.Model):
    """Модель для связи ингредиента с рецептом."""
    ingredients = ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


class TagRecipe(models.Model):
    """Модель для связи тега с рецептом."""
    tags = ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tags} {self.post}'


# class Follow(models.Model):
#     user = ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
#     author = ForeignKey(User, on_delete=models.CASCADE, related_name='following')
