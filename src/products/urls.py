from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.retrieve_all_products),
    url(r'^(?P<product_id>\w{1,100})/$', views.retrieve_product_information)
]
