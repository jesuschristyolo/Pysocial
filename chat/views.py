from django.db.models import Q
from django.shortcuts import render, redirect

from chat.models import ChannelNames, Message
from users.models import User


def get_unread_messages(user):
    channel_objects = ChannelNames.objects.filter(Q(first_user=user.pk) | Q(second_user=user.pk))
    unread_messages = {}
    for channel in channel_objects:
        unread_count = Message.objects.filter(
            channel__channel_name=channel.channel_name,
            reciever=user,
            viewed=False
        ).count()
        unread_messages[str(channel.channel_name)] = unread_count
    return channel_objects, unread_messages


def dialogue_start_page(request):
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
    if ChannelNames.objects.filter(Q(first_user=request.user.pk) | Q(second_user=request.user.pk)).exists():
        channel_objects, unread_messages = get_unread_messages(request.user)
    else:
        return redirect("chat:no_chats")

    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('delete_room'):
            ChannelNames.objects.get(channel_name=request.POST['delete_room']).delete()
            return redirect('chat:dialogue_start_page')

    else:
        try:
            current_channel = ChannelNames.objects.get(channel_name=room_name)
            if request.user.pk == int(room_name.split('_')[0]):
                companion = User.objects.get(pk=int(room_name.split('_')[-1]))
            else:
                companion = User.objects.get(pk=int(room_name.split('_')[0]))

            if Message.objects.filter(channel__channel_name=current_channel.channel_name).exists():
                messages = Message.objects.filter(channel__channel_name=current_channel.channel_name).order_by(
                    'timestamp')
                Message.objects.filter(channel__channel_name=current_channel.channel_name,
                                       reciever=request.user).update(viewed=True)
                print('yes')
            else:
                print('no')
                messages = None

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
            return render(request, "chat/room.html", {
                "room_name": room_name,
                "user": request.user,
                "channel_objects": channel_objects,
                "unread_messages": unread_messages
            })
