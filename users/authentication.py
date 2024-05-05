from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    """
      Пользовательский бэкенд аутентификации по электронной почте.

      Класс EmailAuthBackend представляет собой пользовательский бэкенд аутентификации,
      который позволяет пользователям аутентифицироваться по их электронной почте вместо имени пользователя.

      Методы:
      authenticate: Метод аутентификации пользователя по электронной почте и паролю.
      get_user: Метод для получения пользователя по его идентификатору.

      """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            # здесь мы используем username как email
            user = user_model.objects.get(email=username)
            # стандартный метод проверки для модели User
            if user.check_password(password):
                return user
            return None

        # Обработка исключений DoesNotExist(не нашлось резов) MultipleObjecsReturned(нашлось много резов)
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        # метод отображения пользователя рядом с кнопкой войти
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
