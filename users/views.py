from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from chat.models import ChannelNames
from friends.models import FriendRequest
from users.forms import RegisterUserForm, LoginUserForm, ProfileUserForm
from users.models import User
import logging

# используем имя модуля для названия текущего логгера
logging.basicConfig(filename='C:/Python Projects/django_social/py_logs.log', level=logging.INFO, encoding="UTF-8")
logger = logging.getLogger(__name__)


class RegisterUser(CreateView):
    """Класс представления регистрации нового пользователя"""
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Вызываем метод form_valid() родительского класса
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        # Записываем в лог информацию о успешной регистрации
        logger.info(f"Зарегистрировался новый пользователь {username}")
        # Возвращаем ответ
        return response


class LoginUser(LoginView):
    """Класс представления профиля пользователя"""
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        """Возвращает URL-адрес перенаправления после успешного входа."""
        return reverse_lazy('users:user_profile')


class ProfileUser(DetailView):
    """Представление для отображения профиля пользователя."""
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'user_object'

    def get_object(self, queryset=None):
        """Получает объект пользователя и записывает информацию в лог."""
        logger.info(f'Пользователь {self.request.user.username} просматривает страницу своего профиля.')
        return self.request.user


def other_user_profile(request, pk):
    """
    Представление для отображения профиля другого пользователя и управления запросами на дружбу.
    Это представление отображает профиль другого пользователя и позволяет текущему
    пользователю отправлять запросы на дружбу, принимать или отклонять запросы, удалять
    друга из списка друзей и т.д. Записи о действиях пользователя записываются в лог.
    """

    other_profile = User.objects.get(pk=pk)
    user = request.user
    if request.method == 'POST':
        button_pressed = request.POST.get('button_pressed', None)

        if button_pressed == 'nothing_accept':
            FriendRequest.objects.create(sender=user, receiver=other_profile).save()

        elif button_pressed == 'enter_accept':
            FriendRequest.objects.filter(Q(sender=other_profile) & Q(receiver=user)).delete()
            user.friends.add(other_profile)
            other_profile.friends.add(user)
            ChannelNames.objects.create(first_user=other_profile, second_user=user,
                                        channel_name=f"{other_profile.pk}_{user.pk}")
            logger.info(f'Пользователь {user.username} принял запрос в друзья от {other_profile.username}.')

        elif button_pressed == 'enter_reject':
            FriendRequest.objects.filter(Q(sender=other_profile) & Q(receiver=user)).delete()
            logger.info(f'Пользователь {user.username} отклонил запрос в друзья от {other_profile.username}.')

        elif button_pressed == 'sent_reject':
            FriendRequest.objects.filter(Q(sender=user) & Q(receiver=other_profile)).delete()

        elif button_pressed == 'friend_delete':
            user.friends.remove(other_profile)
            other_profile.friends.remove(user)
            logger.info(f'Пользователь {user.username} удалил из списка друзей {other_profile.username}.')

        return redirect('users:other_user_profile', other_profile.pk)

    else:
        friend_status = 'nothing'
        if user.friends:
            if user.friends.filter(id=other_profile.pk).exists():
                friend_status = 'friends'
                print('friends')

        if FriendRequest.objects.filter(
                Q(sender=user) & Q(receiver=other_profile)):  # если мы отправляли на страницу
            friend_status = 'sent_request'
        elif FriendRequest.objects.filter(
                Q(sender=other_profile) & Q(receiver=user)):  # если пользователь страницы отправил нам
            friend_status = 'enter_request'
        print(friend_status)
        return render(request, 'users/other_profile.html',
                      {'other_user_profile': other_profile, 'self_client': user, 'friend_status': friend_status})


class UpdateProfile(UpdateView):
    """
    Представление для обновления профиля пользователя.

    Класс UpdateProfile является подклассом UpdateView Django и используется
    для отображения и обновления профиля пользователя. При успешном обновлении
    профиля записывается информация об изменении имени пользователя в лог.
    """

    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/update_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:user_profile')

    def form_valid(self, form):
        # Получаем старое и новое имя пользователя
        old_username = self.request.user.username
        new_username = form.cleaned_data['username']

        # Вызываем метод form_valid() родительского класса
        response = super().form_valid(form)

        # Проверяем, изменилось ли имя пользователя
        if old_username != new_username:
            # Записываем в лог информацию об изменении имени пользователя
            logger.info(f'Пользователь {old_username} изменил username на {new_username}')

        # Возвращаем ответ
        return response


class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
