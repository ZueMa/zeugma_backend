import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from src.buyers.models import Buyer, Cart, ProductCart, Purchase
from src.sellers.models import Order

@csrf_exempt
def authenticate(request):
    if (request.method == 'POST'):
        request_body = json.loads(request.body.decode('utf-8'))
        
        if (request_body['username'] == 'Admin' and request_body['password'] == 'ZueMaAdmin'):
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

    purchase_list = Purchase.objects.order_by('-id')
    purchases = []

    for purchase in purchase_list:
        items_list = purchase.cart.items.all().order_by('id')
        product_carts_list = get_list_or_404(ProductCart, cart_id=purchase.cart.id)
        total_items = 0
        total_price = 0.0

        for item, product_cart in zip(items_list, product_carts_list):
            total_items += product_cart.num_items
            total_price += item.price * product_cart.num_items

        purchases.append({
            "buyer_id": purchase.buyer.id,
            "purchase_id": purchase.id,
            "cart_id": purchase.cart.id,
            "total_items": total_items,
            "total_price": total_price,
            "is_shipped": purchase.is_shipped,
            "timestamp": purchase.timestamp
        })

    return JsonResponse({
        'purchases': purchases
    })