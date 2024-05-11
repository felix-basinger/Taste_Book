from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RegisterForm, LoginForm, RecipeForm
from .models import Category, Recipe, RecipeCategory


def all_recipes(request):
    recipes = Recipe.objects.all().order_by('-add_time')
    return render(request, 'recipes_app/recipes.html', {'recipes': recipes})


def recipes_by_author(request, user_id):
    recipes = Recipe.objects.filter(author_id=user_id).order_by('-add_time')
    return render(request, 'recipes_app/recipes_by_author.html', {'recipes': recipes})


def random_recipes(request):
    recipes = Recipe.objects.prefetch_related('category').order_by('?')[:5]
    return render(request, 'recipes_app/index.html', {'recipes': recipes})


def single_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes_app/recipe.html', {'recipe': recipe})


def recipes_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    recipes = category.recipe_set.all().order_by('-add_time')
    return render(request, 'recipes_app/category_recipes.html',
                  {'recipes': recipes, 'category_name': category.name})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'recipes_app/register.html', {'form': form})


def my_recipes(request):
    if not request.user.is_authenticated:
        return render(request, 'recipes_app/unregistered.html')
    recipes = Recipe.objects.filter(author=request.user).order_by('-add_time')
    return render(request, 'recipes_app/my_recipes.html', {'recipes': recipes})


def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'recipes_app/login.html', {'form': form})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            form.save_m2m()
            return redirect('my_recipes')
    else:
        form = RecipeForm()

    return render(request, 'recipes_app/add_recipe.html', {'form': form})


def your_view(request):
    current_year = datetime.now().year
    return render(request, 'base.html', {'current_year': current_year})


def my_views(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id,
                               author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe', recipe_id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes_app/edit_recipe.html', {'form': form, 'recipe': recipe})
