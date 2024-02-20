from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=username)  # здесь мы используем юернейм как имэйл
            if user.check_password(password):  # стандартный метод проверки для модели User
                return user
            return None

        except (user_model.DoesNotExist,
                user_model.MultipleObjectsReturned):  # Оработка исключений DoesNotExist(не нашлось резов)  MultipleObjecsReturned(нашлось много резов)
            return None

    def get_user(self, user_id): #метод отображения пользователя рядом с кнопкой войти
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)

        except user_model.DoesNotExist:
            return None
