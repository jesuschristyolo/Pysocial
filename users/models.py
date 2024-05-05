from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
        Расширенная модель пользователя.
        Класс User представляет собой расширенную модель пользователя, которая
        наследует от стандартной модели AbstractUser Django. Дополнительные поля,
        такие как фотография профиля, дата рождения, разряд, информация о пользователе
        и список друзей, добавлены для хранения дополнительной информации о пользователях.
    """

    class Grade(models.TextChoices):
        """Класс для хранения вариантов выбора разряда пользователя."""
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
