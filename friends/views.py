from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from chat.models import ChannelNames
from friends.models import *
from users.models import User
import logging

# используем имя модуля для названия текущего логгера
logging.basicConfig(filename='C:/Python Projects/django_social/py_logs.log', level=logging.INFO, encoding="UTF-8")
logger = logging.getLogger(__name__)


def search_users(request):
    """
        Поиск пользователей.
        Функция search_users отвечает за поиск пользователей по их именам.
        Пользователь вводит имя в форму поиска, затем отправляет запрос на сервер.
    """
    if request.method == 'POST':
        searched = request.POST['searched_users']
        users = User.objects.filter(username__icontains=searched).exclude(pk=request.user.pk)
        return render(request, 'friends/search_users.html', {'searched': searched, 'users': users})
    else:
        return render(request, 'friends/search_users.html', {})


def user_friends(request, id):
    """
       Отображение списка друзей пользователя.

       Функция user_friends отвечает за отображение списка друзей пользователя.
       Если пользователь является владельцем списка друзей (зашел на свою страницу друзей),
       ему отображаются кнопки поиска друзей. Если на чужую, то
       отображается список друзей другого пользователя.
       При отправке формы поиска отображаются только
       друзья, чьи имена содержат введенную пользователем строку.

       """
    # Проверяем, является ли текущий пользователь владельцем списка друзей
    main_user = False
    user = User.objects.get(pk=id)
    if request.user.pk == id:
        main_user = True
    if request.method == 'POST':
        searched = request.POST['searched_friends']
        # Фильтруем список друзей по имени, содержащему введенную строку
        user_friends = user.friends.filter(username__icontains=searched)
        return render(request, 'friends/user_friends.html',
                      {'main_user': main_user, 'user_friends': user_friends, 'user': user})
    else:
        user_friends = user.friends.all()
        return render(request, 'friends/user_friends.html',
                      {'main_user': main_user, 'user_friends': user_friends, 'user': user})


def enter_requests(request):
    """
       Обработка входящих запросов в друзья.

       Функция enter_requests отвечает за обработку входящих запросов в друзья для текущего пользователя.
       Пользователь может принять или отклонить запросы в друзья, отправленные другими пользователями.
       После принятия запроса устанавливается взаимное добавление пользователей в список друзей.

       """
    user = request.user

    if request.method == "POST":
        button_pressed = request.POST.get("button_pressed", None)
        solution, friend_pk = button_pressed.split('_')[0], button_pressed.split('_')[1]
        friend_model = User.objects.get(pk=friend_pk)

        if solution == 'accept':
            # Пользователь принял запрос в друзья
            user.friends.add(friend_model)
            friend_model.friends.add(user)
            # Удаляем запрос из базы данных
            FriendRequest.objects.filter(receiver=user, sender=friend_model).delete()

            # Если для этих пользователей еще не создан канал общения, создаем его
            logger.info(f'Пользователь {user.username} добавил в друзья пользователя {friend_model.username}')

            if not ChannelNames.objects.filter(Q(channel_name=f"{friend_model.pk}_{user.pk}") |
                                               Q(channel_name=f"{user.pk}_{friend_model.pk}")).exists():
                ChannelNames.objects.create(first_user=friend_model, second_user=user,
                                            channel_name=f"{friend_model.pk}_{user.pk}")

                logger.info(f'Создан канал {friend_model.pk}_{user.pk}')

        if solution == 'reject':
            # Пользователь отклонил запрос в друзья
            FriendRequest.objects.filter(receiver=user, sender=friend_model).delete()
            logger.info(
                f'Пользователь {user.username} отклонил входящий запрос от пользователя {friend_model.username}')

        return redirect('friends:enter_requests')

    if request.method == "GET":
        # Если метод запроса GET, отображаем страницу с входящими запросами в друзья.
        # Используя пагинацию, разбивая страницы по 3 запроса

        paginator = Paginator(FriendRequest.objects.filter(receiver=user), 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'friends/enter_requests.html', {'page_obj': page_obj, 'user_object': user})


def sent_requests(request):
    """
    Обработка отправленных запросов в друзья.
    Функция sent_requests отвечает за обработку отправленных текущим пользователем запросов в друзья.
    Пользователь может отменить отправленные запросы в друзья.
    """

    user = request.user
    if request.method == "POST":
        # Если метод запроса POST, пользователь нажал на кнопку отмены отправленного запроса
        friend_pk = request.POST.get("button_pressed", None)
        friend_model = User.objects.get(pk=friend_pk)
        # Удаляем запрос из базы данных
        FriendRequest.objects.filter(receiver=friend_model, sender=user).delete()
        return redirect('friends:sent_requests')

    if request.method == "GET":
        paginator = Paginator(FriendRequest.objects.filter(sender=user), 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'friends/sent_requests.html', {'page_obj': page_obj, 'user_object': user})
