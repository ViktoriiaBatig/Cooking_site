from django.contrib import admin
from .models import Recipe, Comment, Like, Favorite

admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Favorite)
