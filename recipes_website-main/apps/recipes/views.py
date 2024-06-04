from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .models import Recipe, Favorite, Comment, Like
from apps.user.models import User
from apps.recipes.youtube_api import scrape_youtube_videos
from django.db.models import Q


def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'recipes': recipes, 'search_context': 'home'})


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect('recipe_success')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})


def recipe_success(request):
    user = request.user
    recipes = Recipe.objects.filter(user=user.id).all()
    return render(request, 'recipes/recipe_success.html', {
        'recipes': recipes, 'user': user})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    is_liked_by_user = request.user.is_authenticated and Like.objects.filter(user=request.user, recipe=recipe).exists()
    is_favorited_by_user = request.user.is_authenticated and Favorite.objects.filter(user=request.user,
                                                                                     recipe=recipe).exists()
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'is_liked_by_user': is_liked_by_user,
        'is_favorited_by_user': is_favorited_by_user,
    })


def user_recipes(request, username):
    user = User.objects.get(username=username)
    recipes = Recipe.objects.filter(user=user.id).all()
    return render(request, 'recipes/user_recipes.html', {
        'recipes': recipes
    })


def favorite_recipes(request):
    user = request.user
    favorite_recipes_ = Recipe.objects.filter(favorite__user=user)
    return render(request, 'recipes/favorite_recipes.html', {
        'favorite_recipes_list': favorite_recipes_
    })


def like_recipes(request):
    user = request.user
    like_recipes_ = Recipe.objects.filter(like__user=user)
    return render(request, 'recipes/like_recipes.html', {
        'like_recipes_list': like_recipes_
    })


def user_recipes(request, username):
    user = User.objects.get(username=username)
    recipes = Recipe.objects.filter(user=user.id).all()
    return render(request, 'recipes/user_recipes.html', {
        'recipes': recipes, 'user': user,
    })


def recipe_videos(request):
    videos = scrape_youtube_videos(None)
    return render(request, 'recipes/recipe_videos.html', {
        'videos': videos, 'search_context': 'videos',
    })


@login_required
def toggle_like(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    liked, created = Like.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        liked.delete()
        return JsonResponse({'likes_count': Like.objects.filter(recipe=recipe).count(), 'liked': False})
    else:
        return JsonResponse({'likes_count': Like.objects.filter(recipe=recipe).count(), 'liked': True})


@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        favorite.delete()
        return JsonResponse({'favorited': False})
    else:
        return JsonResponse({'favorited': True})


@login_required
def post_comment(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        text = request.POST.get('text')
        comment = Comment.objects.create(user=request.user, recipe=recipe, text=text)
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe.delete()
    return redirect('home')


def search(request):
    q = request.GET.get("q", "")
    context = request.GET.get("context")

    if not context:
        context = request.session.get('search_context', 'recipes')
    else:
        request.session['search_context'] = context

    if context == 'videos':
        results = scrape_youtube_videos(q=q)
    else:
        results = Recipe.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )

    return render(request, 'recipes/search_results.html', {'results': results, 'search_query': q, 'context': context})
