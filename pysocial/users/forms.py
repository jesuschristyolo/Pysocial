from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from  crispy_forms.layout import Submit
from django.urls import reverse_lazy

from users.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин(username)", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        labels = {'email': 'E-mail',
                  'first_name': 'Имя',
                  'last_name': 'Фамилия', }

        widgets = {'email': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'})}


    def clean_email(self):  # проверка что у разных пользователей разыне емэйлы
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email существует")
        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileUserForm(forms.ModelForm):  # disabled - нвозможность редактир имя пользователя

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('users:user_profile')
        self.helper.add_input(Submit('submit', 'Редактировать'))

    username = forms.CharField(label="Логин", widget=forms.TextInput)
    this_year = datetime.today().year
    date_birth = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date()}))
    photo = forms.ImageField()


    class Meta:
        model = get_user_model()
        fields = ['grade', 'date_birth', 'photo', 'about_me', 'first_name', 'last_name', 'username']

        labels = {'first_name': 'Имя',
                  'last_name': 'Фамилия', }

        # widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        #            'last_name': forms.TextInput(attrs={'class': 'form-control'})}




