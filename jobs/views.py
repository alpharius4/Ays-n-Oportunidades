from django.shortcuts import render, get_object_or_404
from .models import OfertaLaboral

def lista_ofertas(request):
    ofertas = OfertaLaboral.objects.all().order_by('-fecha_publicacion')
    context = {'ofertas': ofertas}
    return render(request, 'jobs/lista_ofertas.html', context)

# --- NUEVA FUNCIÓN ---
def detalle_oferta(request, oferta_id):
    # Buscamos la oferta exacta, o damos error 404 si no existe
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)
    
    context = {
        'oferta': oferta
    }
    return render(request, 'jobs/detalle_oferta.html', context)