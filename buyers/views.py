from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Buyer

import json

@csrf_exempt
def register(request):
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

def current_buyer(request):
    if (request.method != 'GET'):
        return HttpResponse(status=501)
    if ('id' not in request.COOKIES):
        return HttpResponse(status=404)
    
    buyer = get_object_or_404(Buyer, id=request.COOKIES['id'])

    return JsonResponse({
        'id': buyer.id,
        'username': buyer.username,
        'first_name': buyer.first_name,
        'last_name': buyer.last_name,
        'address': buyer.address
    })
