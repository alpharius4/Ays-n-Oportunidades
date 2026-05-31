from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import OfertaLaboral, Postulacion
from .forms import OfertaLaboralForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages 
from django.conf import settings

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
        messages.error(request, "Solo las empresas pueden publicar ofertas.")
        return redirect('jobs:lista_ofertas')

    if request.method == 'POST':
        form = OfertaLaboralForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.autor = request.user  # Asignamos la empresa que la creó
            oferta.save() 
            
            # --- MAGIA DE GMAIL: Correo de confirmación a la empresa ---
            try:
                send_mail(
                    subject=f'¡Oferta Publicada con Éxito! - {oferta.titulo_cargo}',
                    message=f'Hola {request.user.username},\n\n'
                            f'Tu aviso para "{oferta.titulo_cargo}" ha sido publicado correctamente en Aysén Oportunidades.\n'
                            f'Los trabajadores locales ya pueden verla y enviarte postulaciones.\n\n'
                            f'Gracias por aportar al empleo en la región.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar correo de creación de oferta: {e}")
            # -----------------------------------------------------------

            messages.success(request, "¡Tu oferta ha sido publicada con éxito!")
            return redirect('accounts:dashboard')
    else:
        form = OfertaLaboralForm()

    return render(request, 'jobs/crear_oferta.html', {'form': form})


# ==============================================================================
# MOTOR DE POSTULACIONES: Procesa la solicitud y notifica al empleador por Gmail
# ==============================================================================


@login_required
def postular_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    
    # 1. Filtro de seguridad: Solo los candidatos pueden postular
    if request.user.rol != 'candidato':
        messages.error(request, "Las empresas no pueden postular a ofertas.")
        return redirect('jobs:detalle_oferta', id=id)
        
    # 2. Verificar si el usuario ya postuló antes
    if Postulacion.objects.filter(oferta=oferta, candidato=request.user).exists():
        messages.warning(request, "Ya has postulado a esta oferta anteriormente.")
        return redirect('jobs:detalle_oferta', id=id)
        
    # 3. Procesar la postulación al hacer clic en el botón (método POST)
    if request.method == 'POST':
        # Guardamos el registro en la base de datos
        Postulacion.objects.create(oferta=oferta, candidato=request.user)
        
        # 4. Magia de Gmail: Notificamos al empleador
        try:
            send_mail(
                subject=f'Nueva postulación: {oferta.titulo_cargo}',
                message=f'Hola {oferta.autor.username},\n\n'
                        f'El candidato {request.user.username} ha postulado a tu oferta "{oferta.titulo_cargo}" '
                        f'en Aysén Oportunidades.\n\n'
                        f'Puedes revisar su perfil entrando a tu panel de empresa.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[oferta.autor.email],
                fail_silently=False,
            )
        except Exception as e:
            # Si hay un error con internet o el correo, la postulación se guarda igual
            print(f"Error al enviar correo: {e}") 
            
        messages.success(request, "¡Postulación enviada con éxito! El empleador ha sido notificado.")
        return redirect('accounts:dashboard')
        
    return redirect('jobs:detalle_oferta', id=id)

# ==============================================================================
# VER POSTULANTES: Muestra a la empresa quiénes postularon a su aviso
# ==============================================================================

@login_required
def ver_postulantes(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    
    # Filtro de seguridad: Solo el creador de la oferta puede ver los CVs
    if request.user != oferta.autor:
        messages.error(request, "No tienes permiso para ver los candidatos de esta oferta.")
        return redirect('accounts:dashboard')
        
    # Traemos todas las postulaciones de esta oferta en específico
    postulaciones = Postulacion.objects.filter(oferta=oferta)
    
    return render(request, 'jobs/ver_postulantes.html', {
        'oferta': oferta,
        'postulaciones': postulaciones
    })




def prueba_email(request):
    try:
        send_mail(
            subject='Prueba de Conectividad - Aysén Oportunidades',
            message='¡Excelente noticia, Benjamín! El sistema de correos de Django está configurado y funcionando perfectamente con Gmail.',
            from_email=settings.DEFAULT_FROM_EMAIL, # Este es el correo "Cartero" de settings.py
            recipient_list=['saldiviabenjamin16@gmail.com'], # <-- ¡Cambia esto por tu Gmail de uso diario!
            fail_silently=False,
        )
        return HttpResponse("¡Correo enviado con éxito! Revisa tu bandeja de entrada en el celular o PC.")
    except Exception as e:
        return HttpResponse(f"Error al enviar el correo. El sistema dice: {e}")