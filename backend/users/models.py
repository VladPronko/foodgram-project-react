from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField


class CustomUser(AbstractUser):
    email = EmailField(
        verbose_name='Эл.почта',
        max_length=254,
        unique=True)
    username = CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150
    )
    first_name = CharField(verbose_name='Имя', max_length=150)
    last_name = CharField(verbose_name='Фамилия', max_length=150)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписчик на автора рецепта'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Автор рецепта'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='unique_follow')
        ]

    def __str__(self):
        return (f'Подписчик: { self.user }\n'
                f'Автор: { self.author }')
