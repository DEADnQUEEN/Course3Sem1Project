import django.http
import django.contrib.auth
from django.shortcuts import render, redirect
from django.contrib import messages
import typing
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
        models.Payment.objects.create(user=user, **json.loads(request.body)).save()
        return django.http.response.JsonResponse({'payments': list(get_last_payments(user, 6))})

    return render(
        request,
        'page/add by self.html',
        {
            'title': 'Добавить оплату',
        }
    )


def add_for_company(request: django.http.HttpRequest, index) -> django.http.HttpResponse:
    user: models.User = request.user

    if not user.is_authenticated:
        return redirect('/not-allowed')

    if len(user.director_list) < index:
        return redirect('/wrong-company')

    company: models.Company = user.director_list[index]

    if request.method == 'POST':
        data = json.loads(request.body)
        workers = models.User.objects.filter(company=company)
        print(not len(workers) > data['index'])
        if not len(workers) > data['index']:
            return django.http.response.HttpResponse(
                'Not Found!',
                'application/json'
            )

        worker = workers[data['index']]

        payment = models.Payment.objects.create(user=worker, **data['payment'])

        payment.save()
        print('Saved!')

        return django.http.response.HttpResponse(
            'Saved!',
            'application/json'
        )

    return render(
        request,
        'page/company.html',
        {
            'company': company,
        }
    )


def refresh_company_code(request: django.http.HttpRequest, index) -> typing.Union[
    django.http.HttpResponse, django.http.Http404
]:
    user: models.User = request.user

    if request.method != 'POST':
        return redirect('/not-allowed')

    if len(user.director_list) < index:
        return django.http.Http404()

    company: models.Company = user.director_list[index]
    company.key = models.create_key()
    company.save()

    return django.http.response.HttpResponse(
        json.dumps({'key': company.key}),
        'application/json'
    )
