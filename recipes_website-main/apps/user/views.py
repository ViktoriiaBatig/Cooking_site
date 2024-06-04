from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from apps.user.forms import ProfileChangeForm
from apps.user.models import User
from apps.recipes.models import Recipe, Favorite, Like


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def user_profile(request, username):
    user = User.objects.get(username=username)
    recipes = Recipe.objects.filter(user=user.id).all()
    recipes_count = recipes.count()
    favorites_count = Favorite.objects.filter(recipe__user=user).count()
    likes_count = Like.objects.filter(recipe__user=user).count()
    statistic = {
        'recipes_count': recipes_count,
        'favorites_count': favorites_count,
        'likes_count': likes_count,
    }

    return render(request, 'user/profile.html', {'user': user, 'recipes': recipes, 'statistic': statistic})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            user = User.objects.get(username=request.user.username)
            recipes = Recipe.objects.filter(user=user.id).all()
            recipes_count = recipes.count()
            favorites_count = Favorite.objects.filter(recipe__user=user).count()
            likes_count = Like.objects.filter(recipe__user=user).count()
            statistic = {
                'recipes_count': recipes_count,
                'favorites_count': favorites_count,
                'likes_count': likes_count,
            }
            return render(request, 'user/profile.html', {'user': user, 'recipes': recipes, 'statistic': statistic})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileChangeForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})
