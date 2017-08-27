from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404
from .models import Product

import json

def retrieve_all_products(request):
    if (request.method != 'GET'):
        return HttpResponse(status=501)

    products = get_list_or_404(Product)
    products_response = []
    for product in products:
        products_response.append({
            'product_id': product.id,
            'name': product.name,
            'category': product.category,
            'price': product.price,
            'short_description': product.short_description,
            'image': 'http://localhost:8000/' + str(product.image)
        })

    return JsonResponse({
        'products': products_response
    })
