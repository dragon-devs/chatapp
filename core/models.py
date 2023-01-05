from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile/', default='images/profile-default.png')

    def __str__(self):
        return str(self.user)
