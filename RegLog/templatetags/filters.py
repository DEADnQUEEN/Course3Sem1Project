from django import template
from .. import models
from payment.views import get_last_payments
from django.db.models import Sum

register = template.Library()


@register.filter
def get_company_list(user: models.User):
    return {
        f'company-{i}': {
            'args': {
                'class': 'link',
                'href': f'/payments/add-for-company-{i}/'
            },
            'value': 'Управление компанией "' + company.name + '"'
        }
        for i, company in enumerate(user.director_list)
    }


@register.filter
def get_company_workers(user: models.User, company: models.Company):
    if not user.is_authenticated or user.id != company.director.id:
        raise ValueError()
    return models.User.objects.filter(company=company)


@register.filter
def get_left_bar(user: models.User):
    if not user.is_authenticated:
        return {
            'login': {
                'login': {
                    'args': {
                        'class': 'link',
                        'href': '/login/'
                    },
                    'value': 'login'
                },
                'register': {
                    'args': {
                        'class': 'link',
                        'href': '/register/'
                    },
                    'value': 'register'
                }
            }
        }

    out = {
        'name': {
            'name': {
                'args': {
                    'class': 'text',
                    'href': '/'
                },
                'value': user.human.name_initials
            },
        },
        'logout': {
            'quit': {
                'args': {
                    'class': 'link',
                    'href': '/logout/'
                },
                'value': 'Выйти'
            }
        }
    }

    if not len(models.Connect.objects.filter(user=user)):
        out['add'] = {
            'payments': {
                'args': {
                    'class': 'link',
                    'href': '/payments/add/'
                },
                'value': 'Добавить оплату'
            }
        }

    out['companies'] = get_company_list(user)

    return out


@register.filter
def get_items(obj: dict):
    return obj.items()


@register.filter
def get_most_payments(user: models.User):
    return get_last_payments(user, 6)


@register.filter
def get_payments(user: models.User):
    return models.Payment.objects.filter(
        user=user
    ).values(
        'date'
    ).annotate(
        sum=Sum('amount')
    ).order_by('date')
