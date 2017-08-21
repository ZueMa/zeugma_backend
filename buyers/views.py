from django.http import JsonResponse

from .models import Buyer

def current_buyer(request):
    id = 1
    if 'id' in request.COOKIES:
        id = request.COOKIES['id']
    buyer = Buyer.objects.get(id=id)
    return JsonResponse({
        'id': buyer.id,
        'username': buyer.username,
        'first_name': buyer.first_name,
        'last_name': buyer.last_name,
        'address': buyer.address
    })
