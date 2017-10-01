import json

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Seller
from src.products.models import Product
from src.sellers.models import Order

@csrf_exempt
def register_seller(request):
    if (request.method != 'POST'):
        return HttpResponse(status=405)

    request_body = json.loads(request.body.decode('utf-8'))
    Seller(
        username=request_body['username'],
        password=request_body['password'],
        first_name=request_body['first_name'],
        last_name=request_body['last_name'],
        company_name=request_body['company_name'],
        address=request_body['address'],
        description=request_body['description']
    ).save()

    return HttpResponse(status=204)

def retrieve_current_seller(request, seller_id):
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    seller = get_object_or_404(Seller, id=seller_id)

    return JsonResponse({
        'seller_id': seller.id,
        'username': seller.username,
        'first_name': seller.first_name,
        'last_name': seller.last_name,
        'company_name': seller.company_name,
        'address': seller.address,
        'description': seller.description
    })

@csrf_exempt
def retrieve_and_create_product(request, seller_id):
    if (request.method == 'GET'):
        products_list = get_list_or_404(Product.objects.order_by('id'), seller_id=seller_id)
        products_response = []

        for product in products_list:
            products_response.append({
                'product_id': product.id,
                'name': product.name,
                'category': product.category,
                'price': product.price,
                'short_description': product.short_description,
                'image': product.image
            })

        return JsonResponse({
            'products': products_response
        })
    elif (request.method == 'POST'):
        seller = get_object_or_404(Seller, id=seller_id)

        request_body = json.loads(request.body.decode('utf-8'))
        product = Product(
            name=request_body['name'],
            category=request_body['category'],
            price=request_body['price'],
            num_stocks=request_body['num_stocks'],
            short_description=request_body['short_description'],
            full_description=request_body['full_description'],
            image='{}{}'.format(settings.MEDIA_URL, request_body['image']),
            seller=seller
        )
        product.save()

        return JsonResponse({
            'product_id': product.id
        }, status=201)
    else: 
        return HttpResponse(status=405)

@csrf_exempt
def update_and_delete_product(request, seller_id, product_id):
    if (request.method == 'PUT'):
        product = get_object_or_404(Product, id=product_id)

        request_body = json.loads(request.body.decode('utf-8'))
        product.name = request_body['name']
        product.category = request_body['category']
        product.price = request_body['price']
        product.num_stocks = request_body['num_stocks']
        product.short_description = request_body['short_description']
        product.full_description = request_body['full_description']
        product.image = '{}{}'.format(settings.MEDIA_URL, request_body['image'])
        product.save()

        return HttpResponse(status=204)
    elif (request.method == 'DELETE'):
        product = get_object_or_404(Product, id=product_id)

        product.num_stocks = 0
        product.seller=None
        product.save(update_fields=['num_stocks', 'seller'])

        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

def retrieve_order_history(request, seller_id):
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    orders_list = get_list_or_404(Order.objects.filter(seller_id=seller_id).order_by('-id'))
    orders_response = []

    for order in orders_list:
        orders_response.append({
            'order_id': order.id,
            'product_id': order.product.id,
            'name': order.product.name,
            'short_description': order.product.short_description,
            'image': order.product.image,
            'num_items': order.num_items,
            'revenue': order.revenue,
            'timestamp': order.timestamp
        })

    return JsonResponse({
        'orders': orders_response
    })
