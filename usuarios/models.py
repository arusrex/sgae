from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, cpf=None, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve ter um e-mail")
        email = self.normalize_email(email)
        user = self.model(email=email, cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cpf=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('O superusuário precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('O superusuário precisa ter is_superuser=True.')

        return self.create_user(email, cpf, password, **extra_fields)

class Usuarios(AbstractUser):
    username = None
    email = models.EmailField('E-mail', unique=True)
    cpf = models.CharField("CPF", max_length=11, unique=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["cpf"]

    objects = CustomUserManager() # type: ignore

    def __str__(self):
        return self.get_full_name()
