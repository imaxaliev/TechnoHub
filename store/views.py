from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from datetime import datetime, timezone
from functools import reduce
import stripe
import json

from . import models, forms, functions


class IndexPageView(generic.TemplateView):
    template_name = 'store/index.html'


def show_category(rq, hierarchy=None):
    try:
        actual_order = models.Order.objects.get(id=rq.session.get('order'))
    except models.Order.DoesNotExist:
        order = models.Order()
        order.save()
        rq.session['order'] = order.id
        actual_order = models.Order.objects.get(id=rq.session.get('order'))

    if rq.user.is_authenticated and actual_order.buyer != rq.user:
        actual_order.buyer = rq.user
        actual_order.save()

    category_slug = hierarchy.split('/')
    category_queryset = list(models.Category.objects.all())
    all_slugs = [cat.slug for cat in category_queryset]
    parent = None

    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(models.Category, slug=slug, parent_cat=parent)
        else:
            product = get_object_or_404(models.Product, slug=slug, category=parent)
            breadcrumbs = product.get_breadcrumbs()
            category_name = [' '.join(bc.split('/')[-1].split('-')) for bc in breadcrumbs]
            titled_breadcrumbs = zip(category_name, breadcrumbs)

            return render(rq, 'store/product.html', {
                'product': product,
                'breadcrumbs': titled_breadcrumbs,
                'actual_order': actual_order,
                'review_form': forms.ReviewForm()
            })

    product_set = parent.product_set.order_by('title').all()
    paginator = Paginator(product_set, 2)
    page_obj = paginator.get_page(rq.GET.get('page'))

    return render(rq, 'store/category.html', {
        'product_set': page_obj,
        'sub_categories': parent.category_set.all(),
        'actual_order': actual_order,
    })


def add_to_cart(rq, order_id, product_id):
    if rq.GET:
        response = dict()
        product = get_object_or_404(models.Product, id=product_id)
        order = get_object_or_404(models.Order, id=order_id)
        product_order_detail, created = models.ProductOrderDetail.objects.get_or_create(order=order, product=product)
        if product not in order.products.all():
            order.products.add(product)
            order.refresh_from_db()
            response['productTitle'] = product.title

        if created:
            product_order_detail.amount = 0

        selected_amount = int(rq.GET.get('productAmount', 1))
        if product_order_detail.amount != product.total_amount:
            if product_order_detail.amount + selected_amount > product.total_amount:
                product_order_detail.amount = product.total_amount
            else:
                product_order_detail.amount += selected_amount
            product_order_detail.save()
            order.refresh_from_db()

        response['orderTotalPrice'] = order.total_price
        response['productOrderAmount'] = product_order_detail.amount

        product_total_amount = product.total_amount - product_order_detail.amount
        response['productTotalAmount'] = product_total_amount if product_total_amount > 0 else 0
        response['productOrderPrice'] = product_order_detail.total_price

        response['cartProductsTotalAmount'] = reduce(
            lambda accum, nxt: nxt.amount + accum,
            order.productorderdetail_set.all(),
            0
        )
        return JsonResponse(response)


class Checkout(UserPassesTestMixin, generic.UpdateView):
    model = models.Order
    form_class = forms.CheckoutForm
    template_name = 'store/checkout.html'
    redirect_field_name = None

    def test_func(self):
        return functions.check_availability_in_session(self)

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('store:home'))

    @method_decorator(csrf_exempt)
    def dispatch(self, rq, **kwargs):
        return super(Checkout, self).dispatch(rq, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Checkout, self).get_context_data(**kwargs)
        order = self.get_object()
        context['object'] = context['order'] = forms.OrderForm(instance=order)
        return context

    def form_valid(self, form):
        order = models.Order.objects.get(id=self.request.session['order'])
        response = dict()
        response['payment_method'] = order.payment_method = form.cleaned_data['payment_method']
        response['shipping_method'] = order.shipping_method = form.cleaned_data['shipping_method']
        order.save()
        return JsonResponse(response)

    def post(self, rq, **kwargs):
        if rq.is_ajax():
            self.object = self.get_object()
            self.form = self.get_form()
            if self.form.is_valid():
                return self.form_valid(self.form)
            else:
                return self.form_invalid(self.form)


@csrf_exempt
def get_stripe_conf(rq):
    if rq.method == 'GET':
        conf = {
            'publicKey': settings.STRIPE_PUBLISHABLE_KEY
        }
        return JsonResponse(conf, safe=False)


@csrf_exempt
def create_checkout_session(rq, pk):
    if rq.method == 'GET':
        order = models.Order.objects.get(pk=pk)
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'orders/%s/checkout/succeeded?session_id={CHECKOUT_SESSION_ID}&status=in_process' % pk,
                cancel_url=domain_url + 'orders/%s/checkout/cancelled/' % pk,
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'name': product.title,
                    'quantity': order.productorderdetail_set.get(product=product).amount,
                    'currency': 'rub',
                    'amount': product.total_price * 100
                } for product in order.products.all()]
            )
            return JsonResponse({'session_id': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def get_qiwi_secret(rq, pk):
    if rq.is_ajax():
        response = dict()
        total_price = models.Order.objects.get(id=pk).total_price
        response['secretKey'] = settings.QIWI_SECRET_KEY
        response['totalPrice'] = total_price
        response['expirationDateTime'] = datetime.now(timezone.utc).astimezone()
        response['successUrl'] = settings.DOMAIN_URL + 'orders/%s/checkout/succeeded?status=in_process' % pk
        return JsonResponse(response)


class PaymentSucceeded(UserPassesTestMixin, generic.DetailView):
    template_name = 'store/payment_succeeded.html'
    model = models.Order

    def test_func(self):
        return functions.check_ownership(self)

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('store:home'))

    def get(self, request, *args, **kwargs):
        if request.GET.get('status', None) == 'in_process' and request.session.get('order', None) == order.id:
            order = self.get_object()
            if order.payment_method != order.PaymentMethod.IN_PROCESS:
                order.payment_status = order.PaymentStatus.PAYED
            for product, product_order_detail in zip(order.products.all(), order.productorderdetail_set.all()):
                if product_order_detail.amount > product.in_stock_amount:
                    if product.in_stock_amount != 0:
                        remainder = product_order_detail.amount - product.in_stock_amount
                        product.in_stock_amount = 0
                        product.warehouse_amount -= remainder
                    else:
                        product.warehouse_amount -= product_order_detail.amount
                else:
                    product.in_stock_amount -= product_order_detail.amount
                product.save()
            order.draft = False
            order.status = order.Status.IN_PROCESS
            order.save()
            del request.session['order']
        return super(PaymentSucceeded, self).get(request)


class PaymentCancelled(UserPassesTestMixin, generic.DetailView):
    template_name = 'store/payment_cancelled.html'
    model = models.Order

    def test_func(self):
        return functions.check_availability_in_session(self)

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('store:home'))


class OrderDeletion(UserPassesTestMixin, generic.DeleteView):
    model = models.Order
    template_name = 'store/delete_confirmation.html'

    def test_func(self):
        return functions.check_availability_in_session(self)

    def handle_no_permission(self):
        return HttpResponseRedirect(self.get_login_url())

    def get_login_url(self):
        next_param = self.request.GET.get('next', None)
        self.login_url = next_param if next_param else reverse('store:home')
        return self.login_url

    def get_success_url(self):
        if self.request.GET.get('success_url'):
            return self.request.GET.get('success_url')
        return reverse('store:home')


def find_path(rq):
    q = rq.GET.get('q', None)

    for i, md in enumerate([models.Category, models.Product]):
        try:
            res = md.objects.get(title__icontains=q)
        except md.MultipleObjectsReturned:
            return JsonResponse({'error': 'You must be more concise in searching query.'})
        except md.DoesNotExist:
            if i == 1:
                return JsonResponse({'error': 'No result is available for typed-in searching query.'})
        else:
            hierarchy = res.get_breadcrumbs()[-1] + '/%s' % res.slug if res.get_breadcrumbs() else res.slug
            return JsonResponse({'url': reverse_lazy('store:category', args=[hierarchy])})


class CategoriesList(generic.ListView):
    model = models.Category
    template_name = 'store/categories.html'
    context_object_name = 'categories'
    ordering = ['title']

    def get_queryset(self):
        qs = super(CategoriesList, self).get_queryset()
        updated_qs = []
        for obj in qs:
            if not obj.parent_cat:
                obj.hierarchy = obj.get_breadcrumbs()[-1] + '/%s' % obj.slug if obj.get_breadcrumbs() else obj.slug
                updated_qs.append(obj)
        return updated_qs


class AccountRegister(generic.CreateView):
    model = models.User
    template_name = '../templates/registration/registration.html'
    form_class = forms.AccountForm
    success_url = '/account/login'


@csrf_exempt
def create_review(rq, product_id):
    if rq.method == 'POST':
        data = json.loads(rq.body.decode('utf-8'))
        print(data)
        form = forms.ReviewForm(data)
        response = {}
        if form.is_valid():
            review = models.Review(
                author=rq.user,
                text=form.cleaned_data['text'],
                rate=form.cleaned_data['rate'],
                product_id=product_id
            )
            review.save()

            response['user'] = rq.user.username
            for k in form.cleaned_data:
                response[k] = form.cleaned_data[k]
        else:
            print(form.errors)
        return JsonResponse(response)
