from django.http import HttpResponse, JsonResponse

from .models import Buyer

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
