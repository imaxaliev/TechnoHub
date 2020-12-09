from django import template

from .. import models


register = template.Library()


@register.filter(name='default_img')
def default_img(obj):
    try:
        return obj.get(is_default=True)
    except AttributeError:
        return obj.is_default
    except models.ProductImage.DoesNotExist:
        if not obj:
            return
        raise Exception('At least one product image must be set to default.')
