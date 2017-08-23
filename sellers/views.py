from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Seller

import json

@csrf_exempt
def register(request):
    if (request.method != 'POST'):
        return HttpResponse(status=501)
  
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    Seller(
        username=body['username'],
        password=body['password'],
        first_name=body['first_name'],
        last_name=body['last_name'],
        company_name=body['company_name'],
        address=body['address'],
        description=body['description']
    ).save()

    return HttpResponse(status=204)

def current_seller(request):
    if ('id' not in request.COOKIES):
        return HttpResponse(status=404)
    
    seller = Seller.objects.get(id=request.COOKIES['id'])

    return JsonResponse({
        'id': seller.id,
        'username': seller.username,
        'first_name': seller.first_name,
        'last_name': seller.last_name,
        'company_name': seller.company_name,
        'address': seller.address,
        'description': seller.description
    })
    