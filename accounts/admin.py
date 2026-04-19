from django.contrib import admin
from .models import CustomUser

# Le decimos a Django que muestre el CustomUser en el panel
admin.site.register(CustomUser)