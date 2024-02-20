from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from pysocial import settings
from social_network.views import *
from rest_framework import routers

urlpatterns = [
    path('users/', include('users.urls', namespace="users")),
    path('', include('social_network.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)












