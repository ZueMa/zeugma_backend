from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.authenticate),
    url(r'^purchases/$', views.retrieve_all_purchases),
    url(r'^purchases/(?P<purchase_id>\w{1,100})/$', views.ship_purchase),
    url(r'^products/$', views.retrieve_all_unconfirm_products),
    url(r'^/admin/products/(?P<product_id>\w{1,100})/$', views.confirm_specified_product)
]
