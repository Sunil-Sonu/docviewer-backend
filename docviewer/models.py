from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserFolder(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    folderId = models.CharField(primary_key=True, max_length=50)
    folderPath = models.CharField(max_length=50)

    def __str__(self):
        return self.folderId
