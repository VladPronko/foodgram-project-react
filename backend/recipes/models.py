from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import (CASCADE, CharField, ForeignKey, ImageField,
                              IntegerField, ManyToManyField,
                              PositiveIntegerField, SlugField, TextField)

from users.models import CustomUser


class Tag(models.Model):
    name = CharField(verbose_name='Название', max_length=50, unique=True)
    color = CharField(verbose_name='Цвет в HEX', max_length=10, unique=True)
    slug = SlugField(verbose_name='Уник. слаг', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = CharField(verbose_name='Название', max_length=200)
    measurement_unit = CharField(
        verbose_name='Единицы измерения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = CharField(max_length=200, verbose_name='Название')
    image = ImageField(
        verbose_name='Картинка, закодированная в Base64',
    )
    text = TextField(max_length=1000, verbose_name='Описание')
    ingredients = ManyToManyField(
        Ingredient,
        through='IngredientsForRecipes',
        related_name='recipes',
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

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientsForRecipes(models.Model):
    """
    Модель для ManyToMany связи ингридиентов с рецептами.
    """
    ingredients = ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    recipe = ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    amount = IntegerField(
        validators=[MinValueValidator(
            1, 'Минимальное кол-во ингрид-та - 1')],
        verbose_name='Количество ингридиента'
    )

    class Meta:
        verbose_name = 'Количество ингридиентов в рецепте'

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


class TagRecipe(models.Model):
    """
    Модель для ManyToMany связи тегов с рецептами.
    """
    tags = ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связь тегов с рецептамиы'

    def __str__(self):
        return f'{self.tags} {self.recipe}'


class Favourites(models.Model):
    user = ForeignKey(CustomUser, on_delete=CASCADE, related_name='favorites')
    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_favourites')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    user = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name='shopping_cart'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='shopping_cart')

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'
