from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import online_users.models
from .forms import *
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


# @login_required()
def frontpage(request):
    user_objects = User.objects.all()
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    users_online = (user for user in user_status)
    context = {"online_users"}

    return render(request, 'core/frontpage.html', {'user': user_objects, 'users_online': users_online})


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
