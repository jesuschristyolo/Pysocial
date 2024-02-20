from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from django.contrib.auth.views import LoginView
from users.forms import RegisterUserForm, LoginUserForm, ProfileUserForm
from users.models import User


# from users.models import Profile


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
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


class UpdateProfile(UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/update_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:user_profile')














