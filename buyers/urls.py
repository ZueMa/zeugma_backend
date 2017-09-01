from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register_buyer),
    url(r'^me/$', views.retrieve_current_buyer),
    url(r'^me/cart/$', views.retrieve_cart),
    url(r'^me/cart/items/$', views.add_item_to_cart),
    url(r'^me/cart/items/(?P<item_id>\w{1,100})/$', views.update_and_delete_item)
]
