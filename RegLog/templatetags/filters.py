from django import template
from .. import models
from payment.views import get_last_payments
from django.db.models import Sum

register = template.Library()
base = {
    ''
}


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

    return {
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
        },
        'add': {
            'payments': {
                'args': {
                    'class': 'link',
                    'href': '/payments/add/'
                },
                'value': 'Добавить оплату'
            }
        }
    }


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
