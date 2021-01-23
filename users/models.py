from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class Roles(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    bio = models.TextField(max_length=800, blank=True)
    role = models.CharField(
        max_length=50, 
        choices=Roles.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    
    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR

    @property
    def is_admin(self):
        return self.role == Roles.ADMIN or self.is_staff or self.is_superuser
    
    class Meta:
        ordering = ['username']
