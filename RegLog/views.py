import django.http
from django.shortcuts import render
import django.contrib.auth
from . import models, forms


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

    if user is not None:
        django.contrib.auth.login(request, user)

    return render(request, 'page/html.html')


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
                'title': 'Вход',
                'form': form
            }
        )

    user = form.save()

    if user is not None:
        django.contrib.auth.login(request, user)

    return render(request, 'page/html.html')


def logout(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    django.contrib.auth.logout(request)
    return django.shortcuts.redirect("/login")
