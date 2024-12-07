import profile
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import random

# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super user must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404

class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(_('email address'), unique=True)
    last_seen = models.DateTimeField(null=True, blank=True, default=None)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()

    def is_online(self):
        # Define an "online" threshold in minutes
        online_threshold = timezone.now() - timedelta(minutes=5)
        user_profile = get_object_or_404(CustomUser, id=self.id)
        
        # Check if user's last seen is within the online threshold
        if user_profile.last_seen:
            return user_profile.last_seen >= online_threshold
        return False


    



