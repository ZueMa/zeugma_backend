from django.http import JsonResponse

from .models import Buyer

def current_buyer(request):
    buyer = Buyer.objects.get(id=1)
    return JsonResponse({
        'id': buyer.id,
        'username': buyer.username,
        'first_name': buyer.first_name,
        'last_name': buyer.last_name,
        'address': buyer.address
    })
