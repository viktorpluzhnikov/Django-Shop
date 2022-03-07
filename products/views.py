import json
from django.shortcuts import render
from django.conf import settings

from products.models import Product, ProductCategory


def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'products/index.html', context)


def products(request, category_id=None):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    context = {'title': 'GeekShop - Продукты',
               'categories': ProductCategory.objects.all(),
               'products': products
               }
    return render(request, 'products/products.html', context)



