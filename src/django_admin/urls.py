from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.authenticate),
    url(r'^purchases/$', views.retrieve_all_purchases)
]
