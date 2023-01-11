from datetime import timedelta, datetime

import online_users
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *


@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})


@login_required
def room(request, slugs):
    room = Room.objects.get(slug=slugs)
    messages = Message.objects.filter(room=room).prefetch_related('user').order_by('-id')[:100][::-1]

    return render(request, 'room/room.html', {'room': room, 'messages': messages})
