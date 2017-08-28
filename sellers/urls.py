from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register),
    url(r'^me/$', views.current_seller),
    url(r'^me/products/$', views.create_product),
    url(r'^me/products/(?P<product_id>\w{1,100})/$', views.update_product)
]
