from django.conf.urls.static import static
from django.urls import path, include, re_path

from pysocial import settings

urlpatterns = [
    path('users/', include('users.urls', namespace="users")),
    path('friends/', include('friends.urls', namespace="friends")),
    path('chat/', include('chat.urls', namespace="chat")),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('ribbon/', include('ribbon.urls', namespace="ribbon")),
    path('', include('social_network.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
