from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Настраиваем управление пользователями через панель
        администратора Джанго."""

    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_active'
    )
    list_editable = ('is_staff', 'is_active')
