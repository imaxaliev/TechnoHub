from django.shortcuts import reverse
from django.contrib.syndication.views import Feed

from . import models


class ProductFeed(Feed):
    title = 'Product list'
    link = '/store/products'

    @staticmethod
    def items():
        return models.Product.objects.all()

    def item_link(self, item):
        return reverse('store:category', args=[item.get_breadcrumbs()])
