import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chat.routing import websocket_urlpatterns

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Инициализируем приложение Django ASGI заранее, чтобы гарантировать,
# что AppRegistry заполнен перед импортом кода, который может импортировать модели ORM.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        # Протокол HTTP
        "http": django_asgi_app,
        # Протокол WebSocket
        "websocket": AllowedHostsOriginValidator(
            # сссылка на текущ аутентифик пользователя
            AuthMiddlewareStack(
                # Маршрутизатор URL, который маршрутизирует WebSocket-запросы
                URLRouter(websocket_urlpatterns))
        ),
    }
)
