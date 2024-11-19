from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    userProduct = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    assets = models.IntegerField(blank=True, null=True)
    income = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']