from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save


class PersonalChat(models.Model):
    chat_name = models.CharField(max_length=20, null=True, blank=True)
    slug = models.SlugField(unique=True)
    is_friend = models.BooleanField(default=True)

    def __str__(self):
        return str(self.chat_name)


class PersonalMessage(models.Model):
    sender = models.CharField(max_length=20, null=True)
    chat = models.ForeignKey(PersonalChat, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='personalmessages')
    chat_name = models.CharField(max_length=20, null=True, blank=True)
    content = models.CharField(max_length=255)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.chat.chat_name)


