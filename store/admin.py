from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from django import forms as f
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import forms as auth_forms

from . import models, forms


class InlineProduct(AdminImageMixin, admin.StackedInline):
    model = models.Product
    extra = 0


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [InlineProduct]


class InlineProductReview(admin.StackedInline):
    model = models.Review
    extra = 0


class InlineProductImage(admin.TabularInline):
    model = models.ProductImage
    extra = 0


class InlineLaptopParams(admin.StackedInline):
    model = models.LaptopParams


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'manufacturer')
    readonly_fields = ('times_purchased', 'discount_value', 'total_price', 'total_amount')
    inlines = [InlineProductReview, InlineProductImage]
    exclude = ('is_popular',)

    def get_inlines(self, request, obj):
        if obj:
            if obj.laptop_params and InlineLaptopParams not in self.inlines:
                self.inlines.append(InlineLaptopParams)
            return self.inlines


class InlineOrder(admin.TabularInline):
    model = models.Order
    extra = 0
    readonly_fields = ('total_price', 'creation_date',)


class UserAdmin(AuthUserAdmin):
    inlines = [InlineOrder]


class ProductOrderDetailForm(auth_forms.ModelForm):
    def __init__(self, *args, parent, **kwargs):
        super(ProductOrderDetailForm, self).__init__(*args, **kwargs)
        if getattr(parent, 'pk'):
            self.parent = parent
            self.fields['product'].queryset = models.Order.objects.get(pk=parent.pk).products.all()
            InlineProductOrderDetail.max_num = len(parent.productorderdetail_set.all())


class ProductOrderDetailFormSet(auth_forms.BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent'] = self.instance
        return kwargs


class InlineProductOrderDetail(admin.TabularInline):
    model = models.ProductOrderDetail
    formset = ProductOrderDetailFormSet
    form = ProductOrderDetailForm
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [InlineProductOrderDetail]
    readonly_fields = ('total_price', 'creation_date',)
    exclude = ('draft',)

    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     form_cls = super(OrderAdmin, self).get_form(request, obj, **kwargs)
    #
    #     choices = [(getattr(obj.Status, attr).value, getattr(obj.Status, attr).value.lower()) for attr in dir(obj.Status) if not attr.startswith('__')]
    #
    #     in_process = 'In process'
    #     in_process_tuple = (in_process, in_process.lower())
    #     in_process_id = choices.index(in_process_tuple)
    #     choices.pop(in_process_id)
    #     choices.insert(0, in_process_tuple)
    #
    #     if obj.payment_method and obj.shipping_method:
    #         if obj.shipping_method != 'City courier delivery':
    #             shipping_choice = 'On the way'
    #             if obj.payment_status == obj.PaymentStatus.PAYED:
    #                 choice = 'Awaiting receipt'
    #             choices.insert(1, (choice, choice.lower()))
    #         else:
    #             shipping_choice = 'Awaiting delivery'
    #         choices.insert(1, (shipping_choice, shipping_choice.lower()))
    #
    #     form_cls.base_fields['status'].widget = f.Select(choices=choices)
    #
    #     return form_cls

    def get_queryset(self, request):
        return super(OrderAdmin, self).get_queryset(request).filter(draft=False)


class InlineReviewComment(admin.StackedInline):
    model = models.ReviewComment
    extra = 0


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    model = models.Review
    inlines = [InlineReviewComment]


admin.site.unregister(models.User)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Manufacturer)