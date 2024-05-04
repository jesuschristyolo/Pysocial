from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from chat.models import ChannelNames
from friends.models import *
from users.models import User


def search_users(request):
    if request.method == 'POST':
        searched = request.POST['searched_users']
        users = User.objects.filter(username__icontains=searched).exclude(pk=request.user.pk)
        return render(request, 'friends/search_users.html', {'searched': searched, 'users': users})
    else:
        return render(request, 'friends/search_users.html', {})


def user_friends(request, id):
    main_user = False
    user = User.objects.get(pk=id)
    if request.user.pk == id:
        main_user = True
    if request.method == 'POST':
        searched = request.POST['searched_friends']
        user_friends = user.friends.filter(username__icontains=searched)
        return render(request, 'friends/user_friends.html',
                      {'main_user': main_user, 'user_friends': user_friends, 'user': user})
    else:
        user_friends = user.friends.all()
        return render(request, 'friends/user_friends.html',
                      {'main_user': main_user, 'user_friends': user_friends, 'user': user})


def enter_requests(request):
    user = request.user

    if request.method == "POST":
        print(request.POST.get("button_pressed", None))
        button_pressed = request.POST.get("button_pressed", None)
        solution, friend_pk = button_pressed.split('_')[0], button_pressed.split('_')[1]
        friend_model = User.objects.get(pk=friend_pk)

        if solution == 'accept':
            user.friends.add(friend_model)
            friend_model.friends.add(user)
            FriendRequest.objects.filter(receiver=user, sender=friend_model).delete()

            if not ChannelNames.objects.filter(Q(channel_name=f"{friend_model.pk}_{user.pk}") | Q(
                    channel_name=f"{user.pk}_{friend_model.pk}")).exists():
                ChannelNames.objects.create(first_user=friend_model, second_user=user,
                                            channel_name=f"{friend_model.pk}_{user.pk}")

        if solution == 'reject':
            FriendRequest.objects.filter(receiver=user, sender=friend_model).delete()

        return redirect('friends:enter_requests')

    if request.method == "GET":
        paginator = Paginator(FriendRequest.objects.filter(receiver=user), 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'friends/enter_requests.html', {'page_obj': page_obj, 'user_object': user})


def sent_requests(request):
    user = request.user
    if request.method == "POST":
        print(request.POST.get("button_pressed", None))
        friend_pk = request.POST.get("button_pressed", None)
        friend_model = User.objects.get(pk=friend_pk)
        FriendRequest.objects.filter(receiver=friend_model, sender=user).delete()
        return redirect('friends:sent_requests')

    if request.method == "GET":
        paginator = Paginator(FriendRequest.objects.filter(sender=user), 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'friends/sent_requests.html', {'page_obj': page_obj, 'user_object': user})
