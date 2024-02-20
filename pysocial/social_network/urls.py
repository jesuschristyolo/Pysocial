from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    # path('register/', views.RegisterUser.as_view(), name='register')
]
