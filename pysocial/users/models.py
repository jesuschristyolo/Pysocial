from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Grade(models.TextChoices):
        BEGINNER = 'Beginner', 'Beginner'
        JUNIOR = 'Junior', 'Junior'
        MIDDLE = 'Middle', 'Middle'
        SENIOR = 'Senior', 'Senior'
        LEAD = 'Lead', 'Lead'

    photo = models.ImageField(default='default_avatar/photo_net.png', upload_to="users/%Y/%m/%d/", blank=True,
                              null=True, verbose_name="Фотография")

    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    grade = models.CharField(max_length=10, choices=Grade.choices, default=Grade.BEGINNER, verbose_name="Разряд")
    about_me = models.TextField(blank=True, null=True, verbose_name='Обо мне')
    friends = models.ManyToManyField('User', blank=True)





