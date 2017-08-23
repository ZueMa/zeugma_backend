from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from buyers.models import Buyer
from sellers.models import Seller

import json

@csrf_exempt
def authenticate(request):
    if (request.method == 'POST'):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        username = body['username']
        password = body['password']
        type = body['type']

        try:
            if (type == 'buyer'):
                user = Buyer.objects.get(username=username)
            elif (type == 'seller'):
                user = Seller.objects.get(username=username)
            else:
                return HttpResponse(status=400)
            
            if (user.password == password):
                response = JsonResponse({
                    'username': user.username
                }, status=201)
                response.set_cookie('id', user.id)
                response.set_cookie('type', type)

                return response
            else:
                return HttpResponse(status=500)
        except:
            return HttpResponse(status=500)
    elif (request.method == 'DELETE'):
        return HttpResponse(status=501)
    else:
        return HttpResponse(status=501)
