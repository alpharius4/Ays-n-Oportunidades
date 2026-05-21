from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required # ¡El nuevo guardián!
from .forms import RegistroUsuarioForm
from jobs.models import OfertaLaboral, Postulacion

# --- TU VISTA DE REGISTRO ANTERIOR SE QUEDA IGUAL ---
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:dashboard') # Cambiamos a dónde va tras registrarse
    else:
        form = RegistroUsuarioForm()
        
    return render(request, 'registration/registro.html', {'form': form})

# --- NUEVA VISTA: EL CEREBRO DEL DASHBOARD ---
@login_required
def dashboard(request):
    # Si es una empresa...
    if request.user.rol == 'empleador':
        # Buscamos SOLO las ofertas donde el autor sea el usuario logueado
        # y las ordenamos desde la más nueva a la más vieja
        mis_ofertas = OfertaLaboral.objects.filter(autor=request.user).order_by('-fecha_publicacion')
        
        # Le enviamos esa lista al HTML
        return render(request, 'accounts/dashboard_empleador.html', {'mis_ofertas': mis_ofertas})
        
    # Si es un candidato...
    else:
        # Buscamos SOLO las postulaciones de este usuario, ordenadas por la más reciente
        mis_postulaciones = Postulacion.objects.filter(candidato=request.user).order_by('-fecha_postulacion')
        
        # Le enviamos la lista al HTML
        return render(request, 'accounts/dashboard_candidato.html', {'mis_postulaciones': mis_postulaciones})