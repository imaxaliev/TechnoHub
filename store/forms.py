from django import forms

from . import models


class LaptopParamsForm(forms.ModelForm):
    class Meta:
        model = models.LaptopParams
        fields = '__all__'


class CheckoutForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super(CheckoutForm, self).__init__(**kwargs)
        self.fields['payment_method'] = forms.CharField(
            max_length=30,
            widget=forms.Select(
                choices=self.instance.PaymentMethod.choices,
                attrs={'class': 'browser-default'}
            )
        )
        self.initial['payment_method'] = self.instance.PaymentMethod.ON_RECEIPT

        self.fields['shipping_method'] = forms.CharField(
            max_length=30,
            widget=forms.Select(
                choices=self.instance.ShippingMethod.choices,
                attrs={'class': 'browser-default'}
            )
        )
        self.initial['shipping_method'] = self.instance.ShippingMethod.STORE_PICKUP

    class Meta:
        model = models.Order
        fields = []


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        exclude = ('buyer', 'status', 'payment_method', 'shipping_method', 'draft', 'creation_date')


class AccountForm(forms.ModelForm):
    city = forms.CharField(required=False)

    class Meta:
        model = models.User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        help_texts = {
            'username': None
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

class ReviewForm(forms.ModelForm):

    class Meta:
        model = models.Review
        fields = ('text', 'rate',)
        widgets = {
            'rate': forms.RadioSelect(
                attrs={
                    'class': 'browser-default',
                    'default': None
                },
                choices=models.Review.Rate,
            )
        }