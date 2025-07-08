# flake8: noqa
from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        try:
            username = self.cleaned_data["username"]
            password = self.cleaned_data["password"]
            user = authenticate(username=username, password=password)
        except:
            raise forms.ValidationError("Wrong username and password")
        if user is None:
            raise forms.ValidationError("Wrong username and password")
        return self.cleaned_data


class SignUpForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_repeat = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        try:
            password = self.cleaned_data["password"]
            password_repeat = self.cleaned_data["password_repeat"]
        except:
            raise forms.ValidationError("Password required")

        if password != password_repeat:
            raise forms.ValidationError("Passwords do not match.")
        return self.cleaned_data

    def clean_username(self):
        try:
            username = self.cleaned_data["username"]
        except:
            raise forms.ValidationError("Username required")
        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError("Username already exists")
        except ObjectDoesNotExist:
            pass
        return self.cleaned_data["username"]

    def clean_email(self):
        try:
            email = self.cleaned_data["email"]
        except:
            raise forms.ValidationError("Email required")
        try:
            user = User.objects.get(email=email)

            raise forms.ValidationError("Email already exists")
        except ObjectDoesNotExist:
            pass        return self.cleaned_data["email"]
