from django.contrib import admin

from . import models


@admin.register(models.PersonalChat)
class PersonalChatAdmin(admin.ModelAdmin):
    list_display = ['chat_name', 'slug', 'is_friend', 'id']
    prepopulated_fields = {
        'chat_name': ['slug']
    }


@admin.register(models.PersonalMessage)
class PersonalMessageAdmin(admin.ModelAdmin):
    list_display = ['sender','chat_name', 'chat', 'content', 'added_date']
