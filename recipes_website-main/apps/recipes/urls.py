from django.urls import path

from . import views
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('add_recipe/success/', views.recipe_success, name='recipe_success'),
    path('add_recipe/videos/', views.recipe_videos, name='recipe_videos'),
    path('recipe/user/<str:username>/', views.user_recipes, name='user_recipes'),
    path('recipe/favorite/', views.favorite_recipes, name='favorite_recipes'),
    path('recipe/like/', views.like_recipes, name='like_recipes'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/toggle_like/', views.toggle_like, name='toggle_like'),
    path('recipe/<int:recipe_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('recipe/<int:recipe_id>/post_comment/', views.post_comment, name='post_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('search/', views.search, name='search'),

]
