from django import forms
from .models import OfertaLaboral

class OfertaLaboralForm(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
        # Revisa que estos nombres coincidan exactamente con tu models.py
        fields = ['titulo_cargo', 'descripcion', 'sueldo', 'sistema_turnos', 'es_rural', 'incluye_alojamiento']
        
        # Inyectamos diseño Bootstrap 5
        widgets = {
            'titulo_cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Operador de Maquinaria Pesada'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detalla las funciones del cargo...'}),
            'sueldo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sueldo líquido (Ej: 800000)'}),
            'sistema_turnos': forms.Select(attrs={'class': 'form-select'}),
            'es_rural': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'incluye_alojamiento': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }