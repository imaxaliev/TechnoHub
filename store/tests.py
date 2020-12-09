from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser

from .views import Checkout
from .models import Order


class TestCheckout(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.view = Checkout.as_view()
        self.owner = User(username='maxaliev', password='top_secret')
        self.order = Order(buyer=self.owner)
        self.owner.save()
        self.order.save()
        self.order_id = self.order.id
        self.request = self.factory.get('/store/orders/<pk>/checkout/', {'pk': self.order_id})

    def test_access_permission_for_non_owner(self):
        self.request.user = AnonymousUser()

        response = self.view(self.request, pk=self.order_id)
        self.assertEqual(response.status_code, 302)

    def test_access_perm_for_owner(self):
        self.request.user = self.owner

        response = self.view(self.request, pk=self.order_id)
        self.assertEqual(response.status_code, 200)
