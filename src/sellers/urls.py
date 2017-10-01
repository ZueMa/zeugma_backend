from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.register_seller),
    url(r'^(?P<seller_id>\w{1,100})/$', views.retrieve_current_seller),
    url(r'^(?P<seller_id>\w{1,100})/products/$', views.retrieve_and_create_product),
    url(r'^(?P<seller_id>\w{1,100})/products/(?P<product_id>\w{1,100})/$', views.update_and_delete_product),
    url(r'^(?P<seller_id>\w{1,100})/orders/$', views.retrieve_order_history)
]
