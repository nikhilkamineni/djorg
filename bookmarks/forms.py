from django.contrib.auth.models import User
from django import forms
from .models import Bookmark


class BookmarkForm(forms.ModelForm):

    class Meta:
        model = Bookmark
        fields = ("url", "name", "notes")


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username", "password")
