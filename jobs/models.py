from django.db import models
from django.conf import settings

class OfertaLaboral(models.Model):
    TURNOS = (
        ('14x14', '14x14'),
        ('10x10', '10x10'),
        ('7x7', '7x7'),
        ('5x2', '5x2'),
        ('sin_turno', 'Lunes a Viernes'),
    )
    
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo_cargo = models.CharField(max_length=150)
    sistema_turno = models.CharField(max_length=20, choices=TURNOS)
    
    incluye_alojamiento = models.BooleanField(default=False)
    es_zona_rural = models.BooleanField(default=False)
    
    estado_activa = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo_cargo} - {self.get_sistema_turno_display()}"