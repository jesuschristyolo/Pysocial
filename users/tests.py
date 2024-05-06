from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from friends.models import FriendRequest


class ProfileUserTest(TestCase):
    def setUp(self):
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
        self.assertTrue(login_result)

    def test_user_can_view_own_profile(self):
        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context['user_object'], self.user)

    def test_other_user_profile_view(self):
        response = self.client.get(reverse('users:other_user_profile', kwargs={'pk': self.other_user.pk}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/other_profile.html')
        self.assertEqual(response.context['other_user_profile'], self.other_user)

    def test_friend_request_sent(self):
        response = self.client.post(reverse('users:other_user_profile', kwargs={'pk': self.other_user.pk}),
                                    {'button_pressed': 'nothing_accept'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(FriendRequest.objects.filter(sender=self.user, receiver=self.other_user).exists())

    def test_friend_request_accepted(self):
        FriendRequest.objects.create(sender=self.other_user, receiver=self.user)
        response = self.client.post(reverse('users:other_user_profile', kwargs={'pk': self.other_user.pk}),
                                    {'button_pressed': 'enter_accept'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(self.user.friends.filter(id=self.other_user.pk).exists())
        self.assertTrue(self.other_user.friends.filter(id=self.user.pk).exists())

    def test_break_friendship_status_between_users(self):
        response = self.client.post(reverse('users:other_user_profile', kwargs={'pk': self.other_user.pk}),
                                    {'button_pressed': 'friend_delete'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(not self.user.friends.filter(id=self.other_user.pk).exists())
        self.assertTrue(not self.other_user.friends.filter(id=self.user.pk).exists())

    def tearDown(self):
        "Действия после выполнения каждого теста"
        pass
