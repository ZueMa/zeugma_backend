from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register),
    url(r'^me/$', views.current_buyer)
]
