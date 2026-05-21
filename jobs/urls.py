from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.lista_ofertas, name='lista_ofertas'),
    path('crear/', views.crear_oferta, name='crear_oferta'), # ¡NUEVA RUTA AQUÍ! Debe ir antes del <int:id>
    path('<int:id>/', views.detalle_oferta, name='detalle_oferta'),
    path('<int:id>/postular/', views.postular_oferta, name='postular_oferta'),
    path('<int:id>/postulantes/', views.ver_postulantes, name='ver_postulantes'),
    #path('test-email/', views.prueba_email, name='test_email'),
]