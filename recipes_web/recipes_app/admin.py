from django.contrib import admin
from .models import Recipe, Category, RecipeCategory


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'add_time']
    search_fields = ['title', 'description', 'ingredients']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']


class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'category']
    search_fields = ['recipe__title', 'category__name']


# Регистрация моделей с указанием классов администрирования
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
