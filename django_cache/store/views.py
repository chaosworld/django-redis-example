from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

import string, random

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from .models import Product
 
# Create your views here.

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def price_generator(size=3, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
 
 
def create_product(name, desc='', price=0):
    product = Product(name=name, description=desc, price=price)
    product.save()
 
@api_view(['GET'])
def view_books(request):
     
    products = Product.objects.all()
    if len(products) < 1000:
        i = 0
        while i < 1000 - len(products):
            create_product(id_generator(), desc=3*id_generator(), price=int(price_generator()))
            i += 1

    results = [product.to_json() for product in products]
    return Response(results, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_cached_books(request):
    if 'product' in cache:
        # get results from cache 
        products = cache.get('product')
        return Response(products, status=status.HTTP_201_CREATED)
    else:
        products = Product.objects.all()
        results = [product.to_json() for product in products]
        # store data in cache
        cache.set('product', results, timeout=CACHE_TTL)
        return Response(results, status=status.HTTP_201_CREATED)
