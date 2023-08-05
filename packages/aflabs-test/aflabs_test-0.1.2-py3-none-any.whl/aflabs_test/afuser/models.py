from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class AFLabsModel(models.Model):


    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=255, unique=True)


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
