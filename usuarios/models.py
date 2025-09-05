from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuarios(AbstractUser):
    username = None
    email = models.EmailField('E-mail', unique=True)
    cpf = models.CharField("CPF", max_length=11, unique=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["cpf"]

    def __str__(self):
        return self.get_full_name()
