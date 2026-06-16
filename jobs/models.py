from django.db import models
from django.conf import settings # Para conectar con tu usuario

class OfertaLaboral(models.Model):
    # Relación con el usuario (Empresa) que crea la oferta
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ofertas_publicadas')
    
    # Datos generales del cargo
    titulo_cargo = models.CharField(max_length=200, verbose_name="Título del Cargo")
    descripcion = models.TextField(verbose_name="Descripción del trabajo")
    sueldo = models.IntegerField(verbose_name="Sueldo líquido", null=True, blank=True)
    
    # Opciones de turnos para Aysén
    OPCIONES_TURNOS = [
        ('Lunes a Viernes', 'Jornada Normal (L a V)'),
        ('14x14', 'Turno 14x14'),
        ('7x7', 'Turno 7x7'),
        ('20x10', 'Turno 20x10'),
        ('Otro', 'Otro sistema de turnos'),
    ]
    sistema_turnos = models.CharField(max_length=50, choices=OPCIONES_TURNOS, default='Lunes a Viernes')
    
    # Filtros logísticos regionales
    es_rural = models.BooleanField(default=False, verbose_name="Sector Rural")
    incluye_alojamiento = models.BooleanField(default=False, verbose_name="Incluye Alojamiento/Campamento")
    
    # Metadatos automáticos
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo_cargo} - {self.autor.username}"



class Postulacion(models.Model):
    ESTADOS_POSTULACION = [
        ('pendiente', 'Pendiente'),
        ('revision', 'En Revisión'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    oferta = models.ForeignKey(
        OfertaLaboral, 
        on_delete=models.CASCADE, 
        related_name='postulaciones'
    )
    candidato = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='postulaciones'
    )
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20, 
        choices=ESTADOS_POSTULACION, 
        default='pendiente'
    )
    
    # 🆕 AGREGA ESTA LÍNEA AQUÍ AL FINAL:
    cv_archivo = models.FileField(
        upload_to='cvs_candidatos/', 
        verbose_name="Currículum (PDF/Word)", 
        null=True, 
        blank=True
    )
    class Meta:
        # Esto es clave: evita que un mismo candidato postule dos veces a la misma oferta
        unique_together = ('oferta', 'candidato')
        ordering = ['-fecha_postulacion']

    def __str__(self):
        return f"{self.candidato.username} - {self.oferta.titulo_cargo}"