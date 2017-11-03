import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from src.buyers.models import ProductCart, Purchase

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
