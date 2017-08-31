from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Buyer, Cart, ProductCart
from products.models import Product

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
    product_carts = get_list_or_404(ProductCart, cart=cart)
    total_items = 0
    total_price = 0.0
    items_response = []

    for item, product_cart in zip(items, product_carts):
        items_response.append({
            'product_id': item.id,
            'seller_id': item.seller_id,
            'name': item.name,
            'category': item.category,
            'price': item.price,
            'short_description': item.short_description,
            'image': 'http://localhost:8000/images/{}'.format(item.image),
            'num_items': product_cart.num_items
        })
        total_items += product_cart.num_items
        total_price += item.price * product_cart.num_items

    return JsonResponse({
        'cart_id': cart.id,
        'total_items': total_items,
        'total_price': total_price,
        'items': items_response
    })

@csrf_exempt
def add_item(request):
    if (request.method != 'POST'):
        return HttpResponse(status=501)
    if ('user_id' not in request.COOKIES):
        return HttpResponse(status=404)

    buyer = get_object_or_404(Buyer, id=request.COOKIES['user_id'])
    try:
        cart = get_object_or_404(Cart, is_purchased=False, buyer_id=buyer.id)
    except:
        cart = Cart(buyer=buyer)
        cart.save()

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    product_cart = ProductCart(
        cart=cart,
        product=get_object_or_404(Product, id=body['product_id'])
    )
    product_cart.save()

    return HttpResponse(status=204)
