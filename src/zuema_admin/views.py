import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Admin
from src.buyers.models import ProductCart, Purchase
from src.products.models import Product

@csrf_exempt
def authenticate(request):
    if (request.method == 'POST'):
        request_body = json.loads(request.body.decode('utf-8'))
        
        user = get_object_or_404(Admin, username=request_body['username'])
        if (user.password == request_body['password']):
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)
    elif (request.method == 'DELETE'):
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

def retrieve_all_purchases(request): 
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    purchase_list = Purchase.objects.filter(is_shipped=False).order_by('-id')
    purchases = []

    for purchase in purchase_list:
        items_list = purchase.cart.items.all().order_by('id')
        product_carts_list = get_list_or_404(ProductCart, cart_id=purchase.cart.id)
        total_items = 0
        total_price = 0.0

        for item, product_cart in zip(items_list, product_carts_list):
            total_price += item.price * product_cart.num_items

        purchases.append({
            "purchase_id": purchase.id,
            "total_price": total_price,
            "buyer_username": purchase.buyer.username
        })

    return JsonResponse({
        'purchases': purchases
    })

@csrf_exempt
def ship_purchase(request, purchase_id):
    if (request.method != 'PATCH'):
        return HttpResponse(status=405)

    purchase = get_object_or_404(Purchase, id=purchase_id)

    purchase.is_shipped = True
    purchase.save(update_fields=['is_shipped'])

    return HttpResponse(status=204)

def retrieve_all_unconfirmed_products(request): 
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    product_list = Product.objects.filter(is_confirmed=False).order_by('-id')
    products = []

    for product in product_list:
        products.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "short_description": product.short_description
        })

    return JsonResponse({
        'products': products
    })

@csrf_exempt
def confirm_specified_product(request, product_id):
    if (request.method != 'PATCH'):
        return HttpResponse(status=405)

    product = get_object_or_404(Product, id=product_id)

    product.is_confirmed = True
    product.save(update_fields=['is_confirmed'])

    return HttpResponse(status=204)
