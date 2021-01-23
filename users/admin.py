from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    list_display = (
        'pk',
        'username',
        'role',
        'bio',
        'email',
        'confirmation_key'
        )
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
