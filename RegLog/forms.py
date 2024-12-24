from __future__ import annotations

import hashlib

from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class UserLogin(forms.Form):
    login = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'id': 'login',
                'placeholder': "Login",
                "minlength": 3,
                'autocomplete': "off"
            }
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'id': 'password',
                'placeholder': 'Пароль',
                "minlength": 8,
                'autocomplete': "off"
            }
        )
    )


class UserRegister(UserCreationForm):
    login = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'id': 'login',
                'placeholder': "Login",
                "minlength": 3,
                'autocomplete': "off"
            }
        )
    )
    name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'id': 'name',
                'placeholder': "Имя",
                "minlength": 3,
                'autocomplete': "off"
            }
        )
    )
    surname = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'id': 'surname',
                'placeholder': "Фамилия",
                "minlength": 3,
                'autocomplete': "off"
            }
        )
    )
    father_name = forms.CharField(
        label='Отчество',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'id': 'father_name',
                'placeholder': "Отчество (опционально)",
                "minlength": 3,
                'autocomplete': "off"
            }
        )
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'id': 'password',
                'placeholder': 'Пароль',
                "minlength": 8,
                'autocomplete': "off"
            }
        )
    )
    password2 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'id': 'password2',
                'placeholder': 'Пароль (повторно)',
                "minlength": 8,
                'autocomplete': "off"
            }
        )
    )

    def save(self, commit=True):
        if len(models.User.objects.filter(login__exact=self.data['login'])) > 0:
            raise Exception('Login is not unique')

        if self.data['password1'] != self.data['password2']:
            raise Exception("Passwords are not the same")

        human = models.Human.objects.filter(
            name=self.data['name'],
            surname=self.data['surname'],
            father_name=self.data['father_name']
        ).first()

        if human is None:
            human = models.Human(
                name=self.data['name'],
                surname=self.data['surname'],
                father_name=self.data['father_name']
            )
            human.save()

        user = models.User(
            human=human,
            login=self.data['login'],
            password=hashlib.sha3_256(self.data['password1'].encode()).hexdigest()
        )

        user.set_password(self.data['password1'])
        if commit:
            user.save()

        return user

    class Meta:
        model = models.User
        fields = ['login', 'name', 'surname', 'father_name', 'password1', 'password2']

