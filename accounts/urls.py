from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'), # ¡Nueva ruta!
]