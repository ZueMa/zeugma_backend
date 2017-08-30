from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Buyer, Cart

import json

@csrf_exempt
def register_buyer(request):
    if (request.method != 'POST'):
        return HttpResponse(status=501)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    Buyer(
        username=body['username'],
        password=body['password'],
        first_name=body['first_name'],
        last_name=body['last_name'],
        address=body['address']
    ).save()

    return HttpResponse(status=204)

def retrieve_current_buyer(request):
    if (request.method != 'GET'):
        return HttpResponse(status=501)
    if ('user_id' not in request.COOKIES):
        return HttpResponse(status=404)
    
    buyer = get_object_or_404(Buyer, id=request.COOKIES['user_id'])

    return JsonResponse({
        'buyer_id': buyer.id,
        'username': buyer.username,
        'first_name': buyer.first_name,
        'last_name': buyer.last_name,
        'address': buyer.address
    })

def retrieve_cart(request):
    if (request.method != 'GET'):
        return HttpResponse(status=501)
    if ('user_id' not in request.COOKIES):
        return HttpResponse(status=404)

    buyer = get_object_or_404(Buyer, id=request.COOKIES['user_id'])
    try:
        cart = get_object_or_404(Cart, is_purchased=False, buyer_id=buyer.id)
    except:
        cart = Cart(buyer=buyer)
        cart.save()
    items = cart.items.all().order_by('id')
    total_items = 0
    total_price = 0.0
    items_response = []

    for item in items:
        items_response.append({
            'product_id': item.product.id,
            'seller_id': item.product.seller_id,
            'name': item.product.name,
            'category': item.product.category,
            'price': item.product.price,
            'short_description': item.product.short_description,
            'image': 'http://localhost:8000/images/{}'.format(item.product.image),
            'num_items': item.num_items
        })
        total_items += item.num_items
        total_price += item.product.price * item.num_items

    return JsonResponse({
        'cart_id': cart.id,
        'total_items': total_items,
        'total_price': total_price,
        'items': items_response
    }, status=200)
