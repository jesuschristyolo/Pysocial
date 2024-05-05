from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'friends'
urlpatterns = [
    path('search_users/', cache_page(30)(views.search_users), name='search_users'),
    path('user_friends/<int:id>/', cache_page(30)(views.user_friends), name='user_friends'),
    path('enter_requests/', cache_page(30)(views.enter_requests), name='enter_requests'),
    path('sent_requests/', cache_page(30)(views.sent_requests), name='sent_requests'),
]
