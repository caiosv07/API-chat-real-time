from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
# Create your models here.

class ChatSala(models.Model):
    name = models.CharField(max_length=55)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatUser(models.Model):
    sala = models.ForeignKey(ChatSala, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    TEXT = 'text'
    IMAGE = 'image'

    MESSAGE_TYPES = [
        (TEXT, 'text'),
        (IMAGE, 'image'),
    ]

    sala = models.ForeignKey(ChatSala,  on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default=TEXT)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} - {self.message_type}'
    
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()