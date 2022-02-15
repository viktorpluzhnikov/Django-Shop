from django.urls import path

from products.views import products

app_name = 'products'

urlpatterns = [
    path('abc/', products, name='index')
]