from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    user = models.OneToOneField(User)
    userimage = models.ImageField(upload_to = 'userimages', blank=True)
    contact=models.CharField(max_length = 10, blank = True)

    def __str__(self):
        return self.user.first_name
