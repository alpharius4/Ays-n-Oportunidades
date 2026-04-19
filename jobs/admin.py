from django.contrib import admin
from .models import OfertaLaboral

# Le decimos a Django que muestre las Ofertas Laborales en el panel
admin.site.register(OfertaLaboral)