from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_online = False

    class Meta:
        ordering = ('date_added',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=255, default="Say something about yourself!")
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile/',
                                    default='images/profile-default.png')

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
