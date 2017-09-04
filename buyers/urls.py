from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register_buyer),
    url(r'^(?P<buyer_id>\w{1,100})/$', views.retrieve_current_buyer),
    url(r'^(?P<buyer_id>\w{1,100})/cart/$', views.retrieve_cart),
    url(r'^(?P<buyer_id>\w{1,100})/cart/items/$', views.add_item_to_cart),
    url(r'^(?P<buyer_id>\w{1,100})/cart/items/(?P<item_id>\w{1,100})/$', views.update_and_delete_item),
    url(r'^(?P<buyer_id>\w{1,100})/cart/purchase/$', views.purchase_cart),
    url(r'^(?P<buyer_id>\w{1,100})/purchases/$', views.purchase_history)
]
