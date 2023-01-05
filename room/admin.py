from django.contrib import admin

from . import models


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['name']
    }
    list_display = ['name']


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['content', 'date_added', 'user', 'room']


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'profile_pic']
