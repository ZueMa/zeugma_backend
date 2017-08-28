from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register_seller),
    url(r'^me/$', views.retrieve_current_seller),
    url(r'^me/products/$', views.retrieve_and_create_product),
    url(r'^me/products/(?P<product_id>\w{1,100})/$', views.update_and_delete_product)
]
