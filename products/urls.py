from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.retrieve_all_products),
    url(r'^(?P<id>\w{1,100})/$', views.product_info)
]
