from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField


class CustomUser(AbstractUser):
    """Создаем собственную модель пользователя с целью добавления
        новых необходимых полей."""

    first_name = CharField(verbose_name='Имя', max_length=150)
    last_name = CharField(verbose_name='Фамилия', max_length=150)
    email = EmailField(verbose_name='Эл.почта', max_length=254, unique=True)
    username = CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150
    )

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.username
