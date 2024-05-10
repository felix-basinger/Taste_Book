from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Recipe, Category


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', min_length=2, max_length=100)
    password1 = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Неверный логин или пароль")
        if not user.is_active:
            raise forms.ValidationError("Пользователь неактивен")
        return self.cleaned_data

    def get_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        return authenticate(username=username, password=password)


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title',  'category', 'description', 'ingredients', 'preparation_steps', 'cooking_time', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'preparation_steps': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'ingredients': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'category': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['title'].label = 'Название'
        self.fields['description'].label = 'Описание'
        self.fields['cooking_time'].label = 'Время приготовления'
        self.fields['preparation_steps'].label = 'Шаги приготовления (отделяйте знаком ; )'
        self.fields['image'].label = 'Фото блюда'
        self.fields['ingredients'].label = 'Ингредиенты (отделяйте знаком ; )'
        self.fields['category'].label = "Категория"
        self.fields['category'].required = False
