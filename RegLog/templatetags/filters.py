from django import template
from .. import models

register = template.Library()
base = {
    ''
}


@register.filter
def get_left_bar(user: models.User):
    out = {
        'logout': {
            'quit': {
                'args': {
                    'class': 'link',
                    'href': '/logout/'
                },
                'value': 'quit'
            }
        }
    }

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

    return out


@register.filter
def get_items(obj: dict):
    return obj.items()
