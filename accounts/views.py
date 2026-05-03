from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroUsuarioForm

def registro(request):
    # Si el usuario envió el formulario...
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Iniciamos sesión automáticamente tras registrarse
            return redirect('jobs:lista_ofertas') # Lo mandamos a ver los trabajos
    else:
        # Si recién entró a la página, le mostramos el formulario vacío
        form = RegistroUsuarioForm()
        
    return render(request, 'registration/registro.html', {'form': form})