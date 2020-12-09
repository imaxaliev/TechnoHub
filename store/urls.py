from django.urls import path, include, re_path

from . import views, feeds


app_name = 'store'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='home'),
    path('find_path/', views.find_path, name='find_path'),
    path('product/<product_id>/review/create', views.create_review, name='create_review'),
    path('stripe_conf/', views.get_stripe_conf, name='get_stripe_conf'),
    path('categories/', views.CategoriesList.as_view(), name='categories'),
    re_path(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    path('orders/<int:order_id>/add_to_cart/products/<product_id>', views.add_to_cart, name='add_to_cart'),
    path('orders/<pk>/delete/', views.OrderDeletion.as_view(), name='order_deletion'),
    path('orders/<pk>/checkout/', views.Checkout.as_view(), name='checkout'),
    path('orders/<pk>/checkout/create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('orders/<pk>/checkout/get_qiwi_secret/', views.get_qiwi_secret),
    path('orders/<pk>/checkout/succeeded/', views.PaymentSucceeded.as_view()),
    path('orders/<pk>/checkout/cancelled/', views.PaymentCancelled.as_view()),
    path('products/feed/', feeds.ProductFeed()),
]

