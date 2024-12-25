from django import template
from .. import models

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

    out = {
        'name': {
            'name': {
                'args': {
                    'class': 'text',
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

    if user.can_add_payment:
        out['add'] = {
            'payments': {
                'args': {
                    'class': 'link',
                    'href': '/payments/add/'
                },
                'value': 'Добавить оплату'
            }
        }

    return out


@register.filter
def get_items(obj: dict):
    return obj.items()
