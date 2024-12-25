import django.http
import django.contrib.auth
from django.shortcuts import render, redirect
from django.contrib import messages
import RegLog.models


def add(request: django.http.HttpRequest) -> django.http.HttpResponse:
    user: RegLog.models.User = request.user
    if not user.is_authenticated or not user.can_add_payment:
        return redirect('/not-allowed/')

    raise NotImplementedError('')
