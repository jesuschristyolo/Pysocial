from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
]
