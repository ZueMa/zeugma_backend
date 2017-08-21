from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Buyer

import json

@csrf_exempt
def register(request):
    if(request.method != 'POST'):
        return
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    password = body['password']
    first_name = body['first_name']
    last_name = body['last_name']
    address = body['address']
    buyer = Buyer(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        address=address
    )
    buyer.save()
    return HttpResponse(status=204)

def current_buyer(request):
    if 'id' in request.COOKIES:
        id = request.COOKIES['id']
    else:
        return HttpResponse(status=404)
    buyer = Buyer.objects.get(id=id)
    return JsonResponse({
        'id': buyer.id,
        'username': buyer.username,
        'first_name': buyer.first_name,
        'last_name': buyer.last_name,
        'address': buyer.address
    })
