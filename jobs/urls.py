from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.lista_ofertas, name='lista_ofertas'),
    # Agregamos esta nueva línea para el detalle:
    path('<int:oferta_id>/', views.detalle_oferta, name='detalle_oferta'),
]