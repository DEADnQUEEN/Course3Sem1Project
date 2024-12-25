import django.http
from django.shortcuts import render, redirect
import django.contrib.auth
from . import models, forms
from django.contrib import messages


def not_allowed(request: django.http.HttpRequest) -> django.http.HttpResponse:
    return render(request, 'page/not-allowed.html', {'title': 'Why are you here? | Почему ты здесь?'})


def main(request: django.http.HttpRequest) -> django.http.HttpResponse:
    if not request.user.is_authenticated:
        return redirect('/login/')

    return render(
        request,
        'page/main.html',
        {
            'title': 'Main page'
        }
    )


def login(request: django.http.HttpRequest) -> django.http.HttpResponse:
    if request.method == "GET":
        return render(
            request,
            'page/form.html',
            {
                'title': 'Вход',
                'form': forms.UserLogin()
            }
        )

    form = forms.UserLogin(request.POST)

    if not form.is_valid():
        return render(
            request,
            'page/form.html',
            {
                'title': 'Вход',
                'form': form
            }
        )

    user = models.User.objects.filter(login__exact=form.data['login']).first()

    if user is None:
        messages.error(request, 'Логин или пароль неверный')
        return render(
            request,
            'page/form.html', {
                'title': 'Вход',
                'form': form
            }
        )

    django.contrib.auth.login(request, user)
    return redirect('/')


def register(request: django.http.HttpRequest) -> django.http.HttpResponse:
    if request.method == "GET":
        return render(
            request,
            'page/form.html',
            {
                'title': 'Регистрация',
                'form': forms.UserRegister()
            }
        )

    form = forms.UserRegister(request.POST)

    if not form.is_valid():
        return render(
            request,
            'page/form.html',
            {
                'title': 'Регистрация',
                'form': form
            }
        )

    user = form.save()

    if user is None:
        return render(
            request,
            'page/form.html',
            {
                'title': 'Регистрация',
                'form': form
            }
        )

    django.contrib.auth.login(request, user)
    return redirect('/')


def logout(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    django.contrib.auth.logout(request)
    return django.shortcuts.redirect("/login")
