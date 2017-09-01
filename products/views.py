from django.http import HttpResponse, JsonResponse
from .models import Product
from django.shortcuts import get_list_or_404, get_object_or_404

import json

def retrieve_all_products(request):    
    if (request.method != 'GET'):
        return HttpResponse(status=501)

    products_list = get_list_or_404(Product.objects.exclude(num_stocks=0).order_by('id'))
    products_response = []

    for product in products_list:
        products_response.append({
            'product_id': product.id,
            'name': product.name,
            'category': product.category,
            'price': product.price,
            'short_description': product.short_description,
            'image': 'http://localhost:8000/images/{}'.format(product.image)
        })

    return JsonResponse({'products': products_response})

def retrieve_product_information(request, product_id):
    if (request.method != 'GET'):
        return HttpResponse(status=501)

    product = get_object_or_404(Product, id=product_id)

    return JsonResponse({
        'product_id': product.id,
        'name': product.name,
        'category': product.category,
        'price': product.price,
        'num_stocks': product.num_stocks,
        'short_description': product.short_description,
        'full_description': product.full_description,
        'image': 'http://localhost:8000/images/{}'.format(product.image)
    })
