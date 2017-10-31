import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
