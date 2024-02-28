import json
from datetime import timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import online_users.models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@api_view()
def mainpage(request):
    return Response('Okay')


# @login_required()
def frontpage(request):
    user_objects = User.objects.all().prefetch_related('profile')
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    users_online = (user for user in user_status)


    return render(request, 'core/frontpage.html',
                  {'user': user_objects, 'users_online': users_online,
                   })


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required()
def profile(request):
    user = request.user.profile
    form = ProfileForm(instance=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'core/profile.html', context)


def user_profile(request, username):
    username = User.objects.get(username=username)

    return render(request, 'core/user_profile.html', {'user_profile': username})


def home(request):
    return render(request, 'core/base.html', {
        'room_name': "broadcast"
    })


def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")
