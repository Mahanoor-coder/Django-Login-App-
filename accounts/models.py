from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model

class CustomUser(AbstractUser):
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_approved = models.BooleanField(default=False) 