from django.urls import path
from django.conf.urls.static import static
from pysocial import settings
from . import views

app_name = "users"

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('user_profile/', views.ProfileUser.as_view(), name='user_profile'),
    path('update_profile/', views.UpdateProfile.as_view(), name='update_profile'),
]


