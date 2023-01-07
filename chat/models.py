from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class PersonalChat(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)



