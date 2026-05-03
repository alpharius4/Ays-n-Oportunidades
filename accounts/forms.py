from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'rol') 
        
        # Aquí forzamos los diálogos en español a nuestro gusto:
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'rol': '¿Qué tipo de cuenta deseas crear?',
        }