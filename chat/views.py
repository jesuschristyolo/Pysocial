from django.db.models import Q
from django.shortcuts import render, redirect

from chat.models import ChannelNames, Message
from users.models import User
import logging

# используем имя модуля для названия текущего логгера
logging.basicConfig(filename='C:/Python Projects/django_social/py_logs.log', level=logging.INFO, encoding="UTF-8")
logger = logging.getLogger(__name__)


def get_unread_messages(user):
    """
       Получение непрочитанных сообщений для пользователя.
       Функция get_unread_messages принимает пользователя и возвращает непрочитанные сообщения для этого пользователя.
       Для каждого канала общения, в котором участвует пользователь, подсчитывается количество непрочитанных сообщений.
    """

    # Получаем объекты каналов, в которых участвует пользователь
    channel_objects = ChannelNames.objects.filter(Q(first_user=user.pk) | Q(second_user=user.pk))
    unread_messages = {}
    # Для каждого канала общения подсчитываем количество непрочитанных сообщений
    for channel in channel_objects:
        # Фильтруем сообщения для данного канала, которые еще не прочитаны пользователем
        unread_count = Message.objects.filter(
            channel__channel_name=channel.channel_name,
            reciever=user,
            viewed=False
        ).count()
        # Записываем количество непрочитанных сообщений для текущего канала в словарь
        unread_messages[str(channel.channel_name)] = unread_count
    # Возвращаем набор объектов каналов и словарь непрочитанных сообщений
    return channel_objects, unread_messages


def dialogue_start_page(request):
    """
    Отображает страницу начала диалога.

    Функция dialogue_start_page проверяет наличие активных диалогов для текущего пользователя.
    Если у пользователя есть активные диалоги, она получает количество непрочитанных сообщений для каждого диалога
    и отображает страницу с перечнем активных диалогов и количеством непрочитанных сообщений.
    Если у пользователя нет активных диалогов, он перенаправляется на другую страницу.

    """
    if ChannelNames.objects.filter(Q(first_user=request.user.pk) | Q(second_user=request.user.pk)).exists():
        channel_objects, unread_messages = get_unread_messages(request.user)

        return render(request, "chat/dialogue_start_page.html",
                      {"user": request.user,
                       "channel_objects": channel_objects,
                       "unread_messages": unread_messages, })
    else:
        return redirect("chat:no_chats")


def no_chats(request):
    return render(request, "chat/no_chats.html")


def write_first_message(request, friend_id):
    """
    Перенаправляет пользователя для начала диалога.
    Функция write_first_message проверяет наличие канала общения между текущим пользователем и другим пользователем
    с указанным идентификатором (friend_id). Если канал существует, пользователь перенаправляется на страницу
    диалога. Если канал не существует, функция создает новый канал и перенаправляет пользователя на страницу
    диалога с созданным каналом.

    """
    try:
        channel = ChannelNames.objects.get(
            Q(first_user=request.user.pk, second_user=friend_id) |
            Q(first_user=friend_id, second_user=request.user.pk)
        )
        room_name = channel.channel_name
    except:
        # Если канал не существует, создаем его
        channel = ChannelNames.objects.create(
            first_user=request.user,
            second_user=User.objects.get(pk=friend_id),
            channel_name=f"{request.user.pk}_{friend_id}"
        )
        room_name = channel.channel_name

    return redirect("chat:room", room_name=room_name)


def room(request, room_name):
    """
    Отображает страницу комнаты чата.

    Функция room отображает страницу комнаты чата для пользователя. Если у пользователя есть активные диалоги,
    она получает количество непрочитанных сообщений для каждого диалога. Если пользователь перешел на страницу
    комнаты чата, обрабатывает POST-запросы для удаления комнаты чата. В противном случае, функция пытается
    получить информацию о текущем канале чата и его сообщениях для отображения на странице.

    """
    # Проверяем наличие активных диалогов для текущего пользователя
    if ChannelNames.objects.filter(Q(first_user=request.user.pk) | Q(second_user=request.user.pk)).exists():
        # Получаем объекты каналов и количество непрочитанных сообщений для каждого канала
        channel_objects, unread_messages = get_unread_messages(request.user)
    else:
        return redirect("chat:no_chats")

    if request.method == 'POST':
        # Обрабатываем POST-запросы для удаления комнаты чата
        if request.POST.get('delete_room'):
            # Удаляем комнату чата по ее имени
            ChannelNames.objects.get(channel_name=request.POST['delete_room']).delete()
            logger.info(f'Пользователь {request.user.username} Удалил чат {request.POST["delete_room"]}.')
            # Перенаправляем пользователя на страницу начала диалога
            return redirect('chat:dialogue_start_page')

    else:
        try:
            # Пытаемся получить информацию о текущем канале чата и его сообщениях
            current_channel = ChannelNames.objects.get(channel_name=room_name)
            # Определяем собеседника пользователя в данном канале чата
            if request.user.pk == int(room_name.split('_')[0]):
                companion = User.objects.get(pk=int(room_name.split('_')[-1]))
            else:
                companion = User.objects.get(pk=int(room_name.split('_')[0]))

            # Проверяем наличие сообщений в данном канале чата
            if Message.objects.filter(channel__channel_name=current_channel.channel_name).exists():
                # Получаем сообщения для данного канала и помечаем их как прочитанные
                messages = Message.objects.filter(channel__channel_name=current_channel.channel_name).order_by(
                    'timestamp')
                Message.objects.filter(channel__channel_name=current_channel.channel_name,
                                       reciever=request.user).update(viewed=True)
            else:
                messages = None

            # Отображаем страницу комнаты чата с соответствующими данными
            return render(request, "chat/room.html", {
                "room_name": room_name,
                "user": request.user,
                "channel_objects": channel_objects,
                "current_channel": current_channel,
                "companion": companion,
                "messages": messages,
                "unread_messages": unread_messages
            })

        except:
            # Если возникает ошибка при получении информации
            # о канале чата, отображаем страницу с информацией об ошибке
            return render(request, "chat/room.html", {
                "room_name": room_name,
                "user": request.user,
                "channel_objects": channel_objects,
                "unread_messages": unread_messages
            })
