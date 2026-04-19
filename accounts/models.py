from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('empleador', 'Empleador'),
        ('candidato', 'Candidato'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='candidato')

    def __str__(self):
        return f"{self.username} ({self.rol})"