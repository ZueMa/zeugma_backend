import json

from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Buyer, Cart, ProductCart, Purchase
from src.products.models import Product
from src.sellers.models import Order, Seller

@csrf_exempt
def register_buyer(request):
    if (request.method != 'POST'):
        return HttpResponse(status=405)

    request_body = json.loads(request.body.decode('utf-8'))
    Buyer(
        username=request_body['username'],
        password=request_body['password'],
        first_name=request_body['first_name'],
        last_name=request_body['last_name'],
        address=request_body['address']
    ).save()

    return HttpResponse(status=204)

def retrieve_current_buyer(request, buyer_id):
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    buyer = get_object_or_404(Buyer, id=buyer_id)

    return JsonResponse({
        'buyer_id': buyer.id,
        'username': buyer.username,
        'first_name': buyer.first_name,
        'last_name': buyer.last_name,
        'address': buyer.address
    })

def retrieve_cart(request, buyer_id):
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    buyer = get_object_or_404(Buyer, id=buyer_id)
    try:
        cart = Cart.objects.get(is_purchased=False, buyer_id=buyer.id)
    except:
        cart = Cart(buyer=buyer)
        cart.save()
    items_list = cart.items.all().order_by('id')
    try:
        product_carts_list = ProductCart.objects.filter(cart_id=cart.id).order_by('product_id')
    except:
        product_carts_list = []
    total_price = 0.0
    items = []

    for item, product_cart in zip(items_list, product_carts_list):
        items.append({
            'product_id': item.id,
            'name': item.name,
            'price': item.price,
            'num_stocks': item.num_stocks,
            'short_description': item.short_description,
            'image': item.image,
            'num_items': product_cart.num_items
        })
        total_price += item.price * product_cart.num_items

    return JsonResponse({
        'cart_id': cart.id,
        'total_price': total_price,
        'items': items
    })

@csrf_exempt
def add_item_to_cart(request, buyer_id):
    if (request.method != 'POST'):
        return HttpResponse(status=405)

    buyer = get_object_or_404(Buyer, id=buyer_id)
    try:
        cart = Cart.objects.get(is_purchased=False, buyer_id=buyer.id)
    except:
        cart = Cart(buyer=buyer)
        cart.save()

    request_body = json.loads(request.body.decode('utf-8'))
    product = get_object_or_404(Product, id=request_body['product_id'])
    try:
        product_cart = ProductCart.objects.get(cart_id=cart.id, product_id=product.id)

        return HttpResponse(status=304)
    except:
        ProductCart(
            cart=cart,
            product=product
        ).save()

        return HttpResponse(status=204)

@csrf_exempt
def update_and_delete_item(request, buyer_id, item_id):
    if (request.method == 'POST'):
        buyer = get_object_or_404(Buyer, id=buyer_id)
        try:
            cart = Cart.objects.get(is_purchased=False, buyer_id=buyer.id)
        except:
            cart = Cart(buyer=buyer)
            cart.save()
        product = get_object_or_404(Product, id=item_id)
        product_cart = get_object_or_404(ProductCart, cart_id=cart.id, product_id=product.id)

        if (json.loads(request.body.decode('utf-8'))['action'] == 'increase'):
            if (product_cart.num_items == product.num_stocks):
                return HttpResponse(status=304)
            product_cart.num_items = F('num_items') + 1
        else:
            if (product_cart.num_items == 1):
                return HttpResponse(status=304)
            product_cart.num_items = F('num_items') - 1
        product_cart.save(update_fields=['num_items'])

        return HttpResponse(status=204)
    elif (request.method == 'DELETE'):
        buyer = get_object_or_404(Buyer, id=buyer_id)
        cart = get_object_or_404(Cart, is_purchased=False, buyer_id=buyer.id)
        product = get_object_or_404(Product, id=item_id)
        product_cart = get_object_or_404(ProductCart, cart_id=cart.id, product_id=product.id)

        product_cart.delete()

        return HttpResponse(status=204)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def purchase_cart(request, buyer_id):
    if (request.method != 'POST'):
        return HttpResponse(status=405)

    buyer = get_object_or_404(Buyer, id=buyer_id)
    cart = get_object_or_404(Cart, is_purchased=False, buyer_id=buyer.id)
    items_list = cart.items.all().order_by('id')
    product_carts_list = ProductCart.objects.filter(cart_id=cart.id)
    if (len(product_carts_list) == 0):
        return HttpResponse(status=304)

    for item, product_cart in zip(items_list, product_carts_list):
        item.num_stocks = F('num_stocks') - product_cart.num_items
        item.save(update_fields=['num_stocks'])
        Order(
            product=item,
            seller=item.seller,
            num_items=product_cart.num_items,
            revenue=item.price * product_cart.num_items
        ).save()
    purchase = Purchase(
        cart=cart,
        buyer=buyer
    )
    purchase.save()
    cart.is_purchased = True
    cart.save(update_fields=['is_purchased'])

    return JsonResponse({
        'purchase_id': purchase.id
    }, status=201)

def retrieve_purchase_history(request, buyer_id):
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    purchases_list = Purchase.objects.filter(buyer_id=buyer_id).order_by('-id')
    purchases = []

    for purchase in purchases_list:
        items_list = purchase.cart.items.all().order_by('id')
        product_carts_list = get_list_or_404(ProductCart, cart_id=purchase.cart.id)
        total_items = 0
        total_price = 0.0

        for item, product_cart in zip(items_list, product_carts_list):
            total_items += product_cart.num_items
            total_price += item.price * product_cart.num_items

        purchases.append({
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

def retrieve_purchased_cart(request, buyer_id, purchase_id):
    if (request.method != 'GET'):
        return HttpResponse(status=405)

    purchase = get_object_or_404(Purchase, id=purchase_id)
    items_list = purchase.cart.items.all().order_by('id')
    product_carts_list = get_list_or_404(ProductCart, cart_id=purchase.cart.id)
    total_price = 0.0
    items = []

    for item, product_cart in zip(items_list, product_carts_list):
        items.append({
            'product_id': item.id,
            'name': item.name,
            'price': item.price,
            'short_description': item.short_description,
            'image': item.image,
            'num_items': product_cart.num_items
        })
        total_price += item.price * product_cart.num_items

    return JsonResponse({
        "purchase_id": purchase.id,
        "cart_id": purchase.cart.id,
        "total_price": total_price,
        "items": items
    })
