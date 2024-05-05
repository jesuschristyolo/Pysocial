from django.urls import re_path

from . import consumers

# Определяем URL-шаблоны для WebSocket
websocket_urlpatterns = [
    # Путь к потребителю чата, где room_name является названием канала
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]












