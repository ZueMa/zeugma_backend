from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register),
    url(r'^me/$', views.current_seller),
    url(r'^me/products/$', views.create_product)
]
