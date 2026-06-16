"""
URL configuration for aysen_oportunidades project.
"""
from django.contrib import admin
from django.urls import path, include

# 1. 🆕 Importamos las herramientas de configuración y archivos estáticos/media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobs.urls')),
    
    # 1. PRIMERO va nuestra ruta personalizada para el REGISTRO:
    path('accounts/', include('accounts.urls')), 
    
    # 2. DESPUÉS van las rutas que trae Django de fábrica para el LOGIN:
    path('accounts/', include('django.contrib.auth.urls')), 
]

# 2. 🆕 Agregamos las rutas de los archivos Media (solo para entorno de desarrollo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)