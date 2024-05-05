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
logger = logging.getLogger(__name__)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    logger.info("Зарегистрировался новый пользователь")
    success_url = reverse_lazy('users:login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('users:user_profile')


class ProfileUser(DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    context_object_name = 'user_object'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return self.request.user


def other_user_profile(request, pk):
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

        elif button_pressed == 'enter_reject':
            FriendRequest.objects.filter(Q(sender=other_profile) & Q(receiver=user)).delete()

        elif button_pressed == 'sent_reject':
            FriendRequest.objects.filter(Q(sender=user) & Q(receiver=other_profile)).delete()

        elif button_pressed == 'friend_delete':
            user.friends.remove(other_profile)
            other_profile.friends.remove(user)

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
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/update_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:user_profile')


class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
