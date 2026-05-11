from django import forms
from .models import OfertaLaboral

class OfertaLaboralForm(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
        # Usamos exactamente los nombres que están en tu models.py
        fields = ['titulo_cargo', 'sistema_turno', 'es_zona_rural', 'incluye_alojamiento']
        
        labels = {
            'titulo_cargo': 'Título del Cargo',
            'sistema_turno': 'Sistema de Turnos Regional',
            'es_zona_rural': '¿El trabajo se desarrolla en zona rural aislada?',
            'incluye_alojamiento': '¿La empresa provee alojamiento (Campamento/Faena)?',
        }