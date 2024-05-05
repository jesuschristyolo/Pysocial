from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'chat'

urlpatterns = [
    path('no_chats/', cache_page(30)(views.no_chats), name='no_chats'),
    path('dialogue_start_page/', views.dialogue_start_page, name='dialogue_start_page'),
    path('write_first_message/<int:friend_id>/', views.write_first_message, name='write_first_message'),
    path('<str:room_name>/', views.room, name='room'),
]
