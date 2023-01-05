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
            return redirect('frontpage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required()
def profile(request):
    context = {}
    return render(request, 'core/profile.html', {'profile': context})
