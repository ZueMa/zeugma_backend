from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Product

def retrieve_all_products(request):    
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    products_list = Product.objects.order_by('id')
    products = []

    for product in products_list:
        products.append({
            'product_id': product.id,
            'name': product.name,
            'category': product.category,
            'price': product.price,
            'num_stocks': product.num_stocks,
            'short_description': product.short_description,
            'image': product.image
        })

    return JsonResponse({
        'products': products
    })

def retrieve_product_information(request, product_id):
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    product = get_object_or_404(Product, id=product_id)

    return JsonResponse({
        'product_id': product.id,
        'name': product.name,
        'category': product.category,
        'price': product.price,
        'num_stocks': product.num_stocks,
        'short_description': product.short_description,
        'full_description': product.full_description,
        'image': product.image
    })
