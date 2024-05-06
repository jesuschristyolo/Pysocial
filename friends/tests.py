from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from friends.models import FriendRequest
from http import HTTPStatus
from django.urls import reverse

from friends.views import enter_requests


# Create your tests here.

class FriendStatusTest(TestCase):
    def setUp(self):
        "Инициализация перед выполнением каждого теста"
        "Инициализация перед выполнением каждого теста"
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password',
            about_me='OLD_INFORMATION_ABOUT_ME'
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='password',
            about_me='SOME_OTHER_INFORMATION_ABOUT_ME'
        )
        login_result = self.client.login(username='testuser', password='password')
        self.factory = RequestFactory()
        self.assertTrue(login_result)

    def test_search_users(self):
        response = self.client.post(reverse('friends:search_users'), data={'searched_users': 'user'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'otheruser')

    def test_search_user_friends(self):
        self.user.friends.add(self.other_user)
        self.other_user.friends.add(self.user)

        response = self.client.get(reverse('friends:user_friends', args=[self.user.pk]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'friends/user_friends.html')
        self.assertContains(response, 'otheruser')

        response = self.client.post(reverse('friends:user_friends', args=[self.user.pk]),
                                    data={'searched_friends': 'other'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'friends/user_friends.html')
        self.assertContains(response, 'otheruser')

    def test_enter_requests_accept(self):
        # Создаем запрос в друзья от другого пользователя
        FriendRequest.objects.create(sender=self.other_user, receiver=self.user)
        # Создаем запрос POST, чтобы принять запрос в друзья
        url = reverse('friends:enter_requests')
        request = self.factory.post(url, {'button_pressed': f'accept_{self.other_user.pk}'})
        request.user = self.user
        # Вызываем представление
        response = enter_requests(request)
        # Проверяем, что запрос удален из базы данных
        self.assertFalse(FriendRequest.objects.filter(receiver=self.user).exists())
        # Проверяем, что пользователь добавлен в друзья
        self.assertTrue(self.user.friends.filter(pk=self.other_user.pk).exists())
        self.assertTrue(self.other_user.friends.filter(pk=self.user.pk).exists())
        # Проверяем, что запрос перенаправляет на ту же страницу
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('friends:enter_requests'))

    def tearDown(self):
        "Действия после выполнения каждого теста"
