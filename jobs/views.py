from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import OfertaLaboral
from .forms import OfertaLaboralForm

# --------------------------------------------------------
# 1. VISTAS PÚBLICAS (Semana 7)
# --------------------------------------------------------
def lista_ofertas(request):
    # Traemos todas las ofertas de la base de datos
    ofertas = OfertaLaboral.objects.all() 
    return render(request, 'jobs/lista_ofertas.html', {'ofertas': ofertas})

def detalle_oferta(request, id):
    # Buscamos una oferta específica por su ID
    oferta = get_object_or_404(OfertaLaboral, id=id)
    return render(request, 'jobs/detalle_oferta.html', {'oferta': oferta})


# --------------------------------------------------------
# 2. VISTAS PRIVADAS (Semana 9)
# --------------------------------------------------------
@login_required
def crear_oferta(request):
    # Medida de seguridad: Solo Empleadores pueden crear ofertas
    if request.user.rol != 'empleador':
        return redirect('jobs:lista_ofertas')

    if request.method == 'POST':
        form = OfertaLaboralForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.autor = request.user  # Asignamos la empresa que la creó
            oferta.save() 
            return redirect('accounts:dashboard')
    else:
        form = OfertaLaboralForm()

    return render(request, 'jobs/crear_oferta.html', {'form': form})