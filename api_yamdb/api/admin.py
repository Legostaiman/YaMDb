from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Title, Category, Genre, Review, Comment


admin.site.register(Genre,)
admin.site.register(Category,)
admin.site.register(Title,)
admin.site.register(Review,)
admin.site.register(Comment,)
