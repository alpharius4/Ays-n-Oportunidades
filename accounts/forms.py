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

    # 1. MAGIA DE VALIDACIÓN: Evitar correos duplicados
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Buscamos si existe alguien con este correo en tu modelo CustomUser
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("⚠️ Este correo electrónico ya está registrado. Por favor, utiliza otro o inicia sesión.")
        return email

    # 2. MAGIA VISUAL: Inyectar Bootstrap automáticamente
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Al campo de rol le damos estilo de menú desplegable, al resto de caja de texto
            if field_name == 'rol':
                field.widget.attrs['class'] = 'form-select shadow-sm'
            else:
                field.widget.attrs['class'] = 'form-control shadow-sm'