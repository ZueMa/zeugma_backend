from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^authentication/', include('src.authentication.urls')),
    url(r'^buyers/', include('src.buyers.urls')),
    url(r'^products/', include('src.products.urls')),
    url(r'^sellers/', include('src.sellers.urls'))
]
