from django.shortcuts import render
from .models import *


def chat_view(request):
    users = User.objects.exclude(username=request.user.username)

    return render(request, 'chat/personal_index.html', {'users': users})


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
        p_chat = PersonalChat.objects.create(slug=chat_name, chat_name='chat_' + request.user.username + '_' + user.username)
        print('no')

    chat_message = PersonalMessage.objects.filter(chat=p_chat)

    return render(request, 'chat/personal_chat.html',
                  {'user': user, 'chat_message': chat_message, 'users': users})
