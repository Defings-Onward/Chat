from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2",'profile_picture']





class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]