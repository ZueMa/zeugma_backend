from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
        user_type = body['user_type']

        try:
            if (user_type == 'buyer'):
                user = get_object_or_404(Buyer, username=username)
            elif (user_type == 'seller'):
                user = get_object_or_404(Seller, username=username)
            else:
                return HttpResponse(status=400)

            if (user.password == password):
                response = HttpResponse(status=204)
                response.set_cookie('user_id', user.id)
                response.set_cookie('username', user.username)
                response.set_cookie('user_type', user_type)

                return response
            else:
                return HttpResponse(status=500)
        except:
            return HttpResponse(status=500)
    elif (request.method == 'DELETE'):
        response = HttpResponse(status=204)
        response.set_cookie('user_id', '0')
        response.set_cookie('username', 'guest')
        response.set_cookie('user_type', 'guest')

        return response
    else:
        return HttpResponse(status=501)
