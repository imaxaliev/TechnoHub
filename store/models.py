from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from sorl.thumbnail.fields import ImageField
from functools import reduce
from datetime import datetime
import sys
import inspect
import inflect


class CommonCategoryProduct(models.Model):

    class Meta:
        abstract = True

    def get_breadcrumbs(self):
        parent = self.category if hasattr(self, 'category') else self.parent_cat
        breadcrumbs = ['dummy']
        while parent:
            breadcrumbs.append(parent.slug)
            parent = parent.parent_cat
        for i in range(len(breadcrumbs) - 1):
            breadcrumbs[i] = '/'.join(breadcrumbs[-1:i-1:-1])
        return breadcrumbs[-1:0:-1]


class Category(CommonCategoryProduct):
    parent_cat = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    slug = models.SlugField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        p = inflect.engine()
        title = self.title.capitalize()
        self.title = p.plural_noun(title) if p.plural_noun(self.title) else title
        self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'categories'

    def __str__(self):
        full_path = [self.title]
        parent = self.parent_cat

        while parent:
            full_path.append(parent.title)
            parent = parent.parent_cat
        return '->'.join(full_path[::-1])


class Manufacturer(models.Model):
    name = models.CharField(max_length=30)
    area = models.ManyToManyField(Category)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(CommonCategoryProduct):
    title = models.CharField(max_length=50)
    slug = models.SlugField(default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    model_series = models.CharField(max_length=30)
    description = models.TextField(default=None, null=True, blank=True)

    in_stock_amount = models.PositiveSmallIntegerField(default=0)
    warehouse_amount = models.PositiveIntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)

    price = models.PositiveIntegerField(default=0)
    discount_percent = models.PositiveIntegerField(default=0)
    discount_value = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)

    times_purchased = models.PositiveIntegerField(default=0)
    is_popular = models.BooleanField(default=False)

    @property
    def params(self):
        cls_members = [cl[1] for cl in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
        cls_names = [cl.__name__ for cl in cls_members]
        p = inflect.engine()
        category = p.singular_noun(self.category.title)
        for name in cls_names:
            if name == category + 'Params':
                return getattr(self, category.lower() + '_params')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.discount_value = int(self.price * self.discount_percent / 100) if self.discount_percent != 0 else 0
        self.total_price = self.price - self.discount_value
        self.total_amount = self.in_stock_amount + self.warehouse_amount
        self.times_purchased = reduce(
            lambda accum, nxt:
                accum + nxt.amount,
                ProductOrderDetail.objects.filter(
                    product_id=self.id
                ).filter(
                    order__draft=False
                ),
                0
        )

        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['slug']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = ImageField(upload_to='products/')
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return 'Image #{}'.format(self.id)


class LaptopParams(models.Model):
    product = models.OneToOneField(Product,
                                   on_delete=models.CASCADE,
                                   related_name='laptop_params')
    processor = models.CharField(max_length=40)
    physical_memory = models.CharField(max_length=40)
    ram = models.CharField(max_length=40)
    graphics_card = models.CharField(max_length=40)
    screen_size = models.DecimalField(decimal_places=1, max_digits=4)
    screen_resolution = models.CharField(max_length=30)
    cache_memory = models.CharField(max_length=40)
    dynamics = models.CharField(max_length=30)
    mic = models.CharField(max_length=30)
    additional_utils = models.CharField(max_length=120, default=None)

    corpus = models.CharField(max_length=50)
    thickness = models.DecimalField(max_digits=3, decimal_places=1, help_text='sm')
    weight = models.DecimalField(max_digits=3, decimal_places=1, help_text='kg')

    autonomous_work_time = models.TimeField(help_text='h:m')
    os = models.CharField(max_length=30)

    @property
    def tech_params(self):
        return [
            (self._meta.get_field('processor').verbose_name, self.processor),
            (self._meta.get_field('physical_memory').verbose_name, self.physical_memory),
            (self._meta.get_field('ram').verbose_name, self.ram),
            (self._meta.get_field('graphics_card').verbose_name, self.graphics_card),
            (self._meta.get_field('screen_size').verbose_name, self.screen_size),
            (self._meta.get_field('screen_resolution').verbose_name, self.screen_resolution),
            (self._meta.get_field('cache_memory').verbose_name, self.cache_memory),
            (self._meta.get_field('dynamics').verbose_name, self.dynamics),
            (self._meta.get_field('mic').verbose_name, self.mic),
            (self._meta.get_field('additional_utils').verbose_name, self.additional_utils),
            (self._meta.get_field('autonomous_work_time').verbose_name, self.autonomous_work_time),
            (self._meta.get_field('os').verbose_name, self.os)
        ]

    @property
    def appearance_params(self):
        return [
            (self._meta.get_field('corpus').verbose_name, self.corpus),
            (self._meta.get_field('thickness').verbose_name, self.thickness),
            (self._meta.get_field('weight').verbose_name, self.weight)
        ]

    @property
    def base_params(self):
        return [
            (self._meta.get_field('processor').verbose_name, self.processor),
            (self._meta.get_field('physical_memory').verbose_name, self.physical_memory),
            (self._meta.get_field('ram').verbose_name, self.ram),
            (self._meta.get_field('graphics_card').verbose_name, self.graphics_card),
            (self._meta.get_field('screen_size').verbose_name, self.screen_size),
            (self._meta.get_field('screen_resolution').verbose_name, self.screen_resolution)
        ]

    def __str__(self):
        return ''


class Order(models.Model):
    class PaymentMethod(models.TextChoices):
        ON_RECEIPT = 'On receipt'
        BANK_TRANSACTION = 'Bank Transaction'
        QIWI_WALLET = 'Qiwi wallet'

    class ShippingMethod(models.TextChoices):
        STORE_PICKUP = 'Store pickup'
        CITY_COURIER_DELIVERY = 'City courier delivery'
        PICKUP_POINT = 'Pickup point'

    class Status(models.TextChoices):
        IN_PROCESS = 'In process'
        AWAITS_RECEIPT = 'Awaits receipt'
        COMPLETED = 'Completed'
        REJECTED = 'Rejected'

    class PaymentStatus(models.TextChoices):
        AWAITS_PAYMENT = 'Awaits payment'
        PAYED = 'Payed'

    products = models.ManyToManyField(Product, blank=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    payment_method = models.CharField(max_length=30,
                                      choices=PaymentMethod.choices,
                                      null=True)
    shipping_method = models.CharField(max_length=30,
                                       choices=ShippingMethod.choices,
                                       null=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    payment_status = models.CharField(
        max_length=30,
        choices=PaymentStatus.choices,
        default=PaymentStatus.AWAITS_PAYMENT
    )
    total_price = models.PositiveIntegerField(default=0, help_text='RUB')
    draft = models.BooleanField(default=True)
    custom_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        editable=False
    )
    creation_date = models.DateTimeField(blank=True, null=True)

    def save(self, **kwargs):
        if not self.draft and not self.custom_id:
            prev_id = Order.objects.filter(draft=False).order_by('-custom_id')[0].custom_id
            self.custom_id = int(prev_id) + 1 if prev_id else 1
            self.creation_date = datetime.now()

        return super(Order, self).save(**kwargs)

    def __str__(self):
        return 'Order #{}'.format(self.custom_id)


class ProductOrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.product.total_price * self.amount
        self_save = super(ProductOrderDetail, self).save(*args, **kwargs)
        self.order.total_price = reduce(
            lambda accum, nxt: accum + nxt.total_price,
            self.order.productorderdetail_set.all(),
            0
        )
        self.order.save()
        return self_save

    def __str__(self):
        return self.product.title

    class Meta:
        unique_together = ('order', 'product')
        ordering = ['product__slug']


class Review(models.Model):
    class Rate(models.IntegerChoices):
        REALLY_BAD = 1
        BAD = 2
        AVERAGE = 3
        GOOD = 4
        EXCELLENT = 5

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.IntegerField(choices=Rate.choices, default=None)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']


class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
