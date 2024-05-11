from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.random_recipes, name='index'),
    path('recipes/', views.all_recipes, name='recipes'),
    path('author/<int:user_id>', views.recipes_by_author, name='author'),
    path('recipe/<int:pk>', views.single_recipe, name='recipe'),
    path('categories/<int:category_id>/', views.recipes_by_category, name='recipes_category'),
    path('register/', views.register, name='register'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('accounts/login/', views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('add-recipe/', views.add_recipe, name='add-recipe'),
    path('recipe/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
]
