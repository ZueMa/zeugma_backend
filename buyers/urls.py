from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register_buyer),
    url(r'^me/$', views.retrieve_current_buyer),
    url(r'^me/cart/$', views.retrieve_cart),
    url(r'^me/cart/items/$', views.update_item_quantity)
]
