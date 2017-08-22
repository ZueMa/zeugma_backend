from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Seller

import json
# Create your views here.
@csrf_exempt
def register(request):
  if(request.method != 'POST'):
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