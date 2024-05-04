from django.urls import path
from . import views

app_name = "ribbon"

urlpatterns = [
    path('general_ribbon/', views.general_ribbon, name='general_ribbon'),
    path('create_new_post/', views.create_new_post, name='create_new_post'),
    path('change_post/<int:post_id>/', views.change_post, name='change_post'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),
    path('like_post/', views.like_post, name='like_post'),
    path('like_comment/', views.like_comment, name='like_comment'),
]
