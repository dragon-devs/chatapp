from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save


class Room(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=255, default='Chat group just for fun...')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image_content = models.ImageField(null=True, blank=True, upload_to='images/chatroom/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.content:
            return str(self.user.profile.name + ':' + self.content)
        else:
            return str(self.user.profile.name + ':' + 'images')

    class Meta:
        ordering = ('date_added',)


class RoomImages(models.Model):
    room = models.ForeignKey(Room, related_name='room_images', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='room_images', on_delete=models.CASCADE)
    image_content = models.ImageField(upload_to='images/chatroom/')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.profile.name + ':' + '_images')

    class Meta:
        ordering = ('date_added',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=255, default="Say something about yourself!")
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile/',
                                    default='images/profile.png')

    def __str__(self):
        return str(self.user)


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)


def update_profile(sender, instance, created, **kwargs):
    if not created:
        instance.profile.save()


post_save.connect(update_profile, sender=User)
