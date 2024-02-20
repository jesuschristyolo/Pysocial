from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Grade(models.IntegerChoices):
        BEGINNER = 0, 'Начинающий'
        JUNIOR = 1, 'Джун'
        JUNIOR_PLUS = 2, 'Джун +'
        MIDDLE = 3, 'Мидл'
        SENIOR = 4, 'Синиор'
        LEAD = 5, 'Лид'

    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Фотография")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    grade = models.IntegerField(choices=tuple(map(lambda x: ((x[0]), x[1]), Grade.choices)),
                                default= Grade.BEGINNER, verbose_name= "Разряд")
    about_me = models.TextField(blank=True, null=True, verbose_name='Обо мне')












