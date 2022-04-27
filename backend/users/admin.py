from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'password',
        'is_staff',
        'is_active'
    )
    list_editable = ('is_staff', 'is_active',)
    list_filter = ('email', 'first_name')
