# from django.db import models

# # Create your models here.

# from django.contrib.auth.models import AbstractUser

# from .manager import CustomUserManager

# class CustomUser(AbstractUser):

#     username = None
#     phone_number = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(unique=True)

#     # Use CustomUserManager for user management
#     objects = CustomUserManager()

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = ['email']

#     def __str__(self) -> str:
#         return f'{self.phone_number} - {self.email}'

# class PhoneOTP(models.Model):

#     phone_number =  models.CharField(max_length=15, unique=True)

#     otp = models.CharField(max_length=6)

#     validated= models.BooleanField(default=False)

#     created_at= models.DateTimeField(auto_now_add=True)

#     updated_at= models.DateTimeField(auto_now=True)
    


#     def __str__(self) -> str:
#         return f'{self.phone_number} -{self.otp}'


# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.phone_number} - {self.email}'


class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.otp}'

