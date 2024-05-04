from django.urls import path
from . import views

app_name = 'friends'
urlpatterns = [
    path('search_users/', views.search_users, name='search_users'),
    path('user_friends/<int:id>/', views.user_friends, name='user_friends'),
    path('enter_requests/', views.enter_requests, name='enter_requests'),
    path('sent_requests/', views.sent_requests, name='sent_requests'),
]
