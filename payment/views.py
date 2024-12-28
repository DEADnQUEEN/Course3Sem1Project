import django.http
import django.contrib.auth
from django.shortcuts import render, redirect
from django.contrib import messages
from RegLog import models
import json
from django.db.models import Count, When, Case, F


def get_last_payments(user, count):
    return models.Payment.objects.filter(
        user=user
    ).annotate(
        amount_value=Case(
            When(amount__lt=0, then=F('amount') * -1),
            default=F('amount')
        )
    ).values('amount_value').annotate(
        count=Count('id')
    ).order_by('-count')[:count]


def add(request: django.http.HttpRequest) -> django.http.HttpResponse:
    user: models.User = request.user
    if not user.is_authenticated:
        return redirect('/not-allowed')

    if request.method == 'POST':
        print(request.body)
        models.Payment.objects.create(user=user, **json.loads(request.body)).save()
        return django.http.response.JsonResponse({'app': get_last_payments(user, 5)})

    return render(
        request,
        'page/payment/add by self.html',
        {
            'title': 'Добавить оплату',
        }
    )
