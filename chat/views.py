from datetime import timedelta

import online_users
from django.shortcuts import render
from .models import *


def chat_view(request):
    users = User.objects.exclude(username=request.user.username)
    user_objects = User.objects.all().prefetch_related('profile')
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    users_online = (user for user in user_status)

    active = list()
    for u in users_online:
        active.append(u.user.username)
        print(u.user.username)

    return render(request, 'chat/personal_index.html', {'users': users, 'online_users': active})


def personal_chat_view(request, username):
    user = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)

    if request.user.id > user.id:
        chat_name = f"chat_{request.user.id}-{user.id}"
    else:
        chat_name = f"chat_{user.id}-{request.user.id}"

    if PersonalChat.objects.filter(slug=chat_name):
        p_chat = PersonalChat.objects.get(slug=chat_name)
        print('yes')
    else:
        p_chat = PersonalChat.objects.create(slug=chat_name,
                                             chat_name='chat_' + request.user.username + '_' + user.username)
        print('no')
    chat_message = PersonalMessage.objects.select_related('chat').prefetch_related('sender').prefetch_related('sender__profile').filter(chat=p_chat)

    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    users_online = (user for user in user_status)

    active = list()
    for u in users_online:
        active.append(u.user.username)

    return render(request, 'chat/personal_chat.html',
                  {'user': user, 'chat_message': chat_message, 'users': users, 'online_users': active})
