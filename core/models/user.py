from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']
