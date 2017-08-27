from django.http import HttpResponse, JsonResponse
from .models import Product
from django.shortcuts import get_list_or_404


import json

        
def retrieveProducts(request):
    
    if (request.method != 'GET'):
        return HttpResponse(status=501)
     
    products_list = get_list_or_404(Product)
    products_response=[]

    for product in products_list:
        products_response.append({
        "product_id": product.id,
        "name": product.name,
        "category":product.category,
        "price": product.price,
        "short_description": product.short_description,
        "image": 'http://localhost:8000/' + str(product.image)
        })
        
              
    return JsonResponse({'products': products_response})
   
