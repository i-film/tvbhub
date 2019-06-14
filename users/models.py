from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.FileField(upload_to='avatar/')
    token = models.CharField(max_length=64, default='0123456789')  # reset password

    class Meta:
        db_table = 'USERS'
