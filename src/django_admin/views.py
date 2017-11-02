import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from src.buyers.models import Purchase

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

@csrf_exempt
def ship_purchase(request, purchase_id):
    if (request.method != 'PATCH'):
        return HttpResponse(status=405)

    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase.is_shipped = True
    purchase.save(update_fields=['is_shipped'])
    return HttpResponse(status=204)
