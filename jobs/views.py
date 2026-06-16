from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import OfertaLaboral, Postulacion
from .forms import OfertaLaboralForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages 
from django.conf import settings
from django.db.models import Q

# --------------------------------------------------------
# 1. VISTAS PÚBLICAS (Semana 7) y Cambio para el buscador de la semana 12 ( solo la de lista_ofertas la de detalle_oferta sigue igual)
# --------------------------------------------------------
def lista_ofertas(request):
    # Por defecto, traemos todas las ofertas activas, de la más nueva a la más vieja
    ofertas = OfertaLaboral.objects.filter(activa=True).order_by('-fecha_publicacion')
    
    # =====================================================================
    # NUEVA MAGIA: Ocultar ofertas a las que el usuario ya postuló
    # =====================================================================
    if request.user.is_authenticated:
        # 1. Buscamos todas las postulaciones de este usuario y sacamos solo los IDs de esas ofertas
        ofertas_postuladas = Postulacion.objects.filter(candidato=request.user).values_list('oferta_id', flat=True)
        
        # 2. Le decimos a Django que "excluya" de la lista principal esas ofertas específicas
        ofertas = ofertas.exclude(id__in=ofertas_postuladas)
    # =====================================================================

    # Capturamos los datos que el usuario envía por la URL (Buscador y Filtros)
    query_texto = request.GET.get('q')
    filtro_rural = request.GET.get('es_rural')
    filtro_turno = request.GET.get('sistema_turnos')

    # Aplicamos el buscador de texto (Busca en título o en la descripción)
    if query_texto:
        ofertas = ofertas.filter(
            Q(titulo_cargo__icontains=query_texto) | 
            Q(descripcion__icontains=query_texto)
        )
    
    # Aplicamos el filtro de Ruralidad (Checkbox)
    if filtro_rural == 'on':
        ofertas = ofertas.filter(es_rural=True)
        
    # Aplicamos el filtro de Turnos (Menú desplegable)
    if filtro_turno:
        ofertas = ofertas.filter(sistema_turnos=filtro_turno)

    # Enviamos las ofertas filtradas (y limpias de postulaciones previas) al HTML
    return render(request, 'jobs/lista_ofertas.html', {'ofertas': ofertas})

def detalle_oferta(request, id):
    # Buscamos una oferta específica por su ID
    oferta = get_object_or_404(OfertaLaboral, id=id)
    
    # Verificamos si el usuario actual ya postuló a esta oferta
    ya_postulado = False
    if request.user.is_authenticated:
        ya_postulado = Postulacion.objects.filter(oferta=oferta, candidato=request.user).exists()
        
    return render(request, 'jobs/detalle_oferta.html', {
        'oferta': oferta,
        'ya_postulado': ya_postulado  # Enviamos el estado al HTML
    })


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
# MOTOR DE POSTULACIONES: Procesa la solicitud y notifica al empleador por Gmail y ahora que pueda recibir archivos
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
        # CAPTURAMOS EL ARCHIVO FÍSICO DESDE EL FORMULARIO HTML
        archivo_cv = request.FILES.get('cv_archivo')
        
        # Guardamos el registro en la base de datos incluyendo el archivo
        Postulacion.objects.create(
            oferta=oferta, 
            candidato=request.user,
            cv_archivo=archivo_cv  # <-- Asegúrate de que se llame así en tu models.py
        )
        
        # 4. Magia de Gmail: Notificamos al empleador (Consola en Render / SMTP local)
        try:
            send_mail(
                subject=f'Nueva postulación: {oferta.titulo_cargo}',
                message=f'Hola {oferta.autor.username},\n\n'
                        f'El candidato {request.user.username} ha postulado a tu oferta "{oferta.titulo_cargo}" '
                        f'en Aysén Oportunidades.\n\n'
                        f'Puedes revisar su perfil y descargar su CV entrando a tu panel de empresa.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[oferta.autor.email],
                fail_silently=False,
            )
        except Exception as e:
            # Si hay un error con internet o el correo, la postulación se guarda igual
            print(f"Error al enviar correo: {e}") 
            
        messages.success(request, "¡Postulación enviada con éxito! Tu currículum ha sido cargado en el sistema.")
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

# ==============================================================================
# pruebas de gmails para notificar al empleador 
# ==============================================================================

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

# ==============================================================================
# VER POSTULANTES: Muestra a la empresa quiénes postularon a su aviso
# ==============================================================================

@login_required
def cambiar_estado_postulacion(request, postulacion_id, nuevo_estado):
    # Buscamos la postulación específica
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    
    # Filtro de seguridad: Solo el autor de la oferta puede cambiar los estados
    if request.user != postulacion.oferta.autor:
        messages.error(request, "No tienes permiso para modificar esta postulación.")
        return redirect('accounts:dashboard')
        
    estados_validos = ['pendiente', 'revision', 'aceptado', 'rechazado']
    
    if nuevo_estado in estados_validos:
        postulacion.estado = nuevo_estado
        postulacion.save()
        messages.success(request, f"Candidato {postulacion.candidato.username} marcado como {nuevo_estado.upper()}.")
        
        # ====================================================================
        # MAGIA DE GMAIL: Notificar al candidato según la decisión de la empresa
        # ====================================================================
        asunto = f"Actualización de tu postulación: {postulacion.oferta.titulo_cargo}"
        mensaje = ""

        # Redactamos un mensaje distinto dependiendo del botón que apretó la empresa
        if nuevo_estado == 'aceptado':
            mensaje = (
                f"¡Felicidades {postulacion.candidato.username}!\n\n"
                f"La empresa {postulacion.oferta.autor.username} ha ACEPTADO tu postulación "
                f"para el cargo de '{postulacion.oferta.titulo_cargo}'.\n\n"
                f"Pronto se pondrán en contacto directo contigo al correo que registraste."
            )
        elif nuevo_estado == 'rechazado':
            mensaje = (
                f"Hola {postulacion.candidato.username},\n\n"
                f"Agradecemos mucho tu interés en el cargo de '{postulacion.oferta.titulo_cargo}'.\n"
                f"Lamentablemente, en esta ocasión la empresa ha decidido avanzar con otros perfiles.\n\n"
                f"¡Te deseamos mucho éxito en tus futuras búsquedas en Aysén Oportunidades!"
            )
        elif nuevo_estado == 'revision':
            mensaje = (
                f"Hola {postulacion.candidato.username},\n\n"
                f"Te informamos que tu currículum para el cargo de '{postulacion.oferta.titulo_cargo}' "
                f"ha pasado a la etapa de REVISIÓN.\n\n"
                f"La empresa está evaluando tu perfil detalladamente. Te notificaremos ante cualquier cambio."
            )

        # Si hay un mensaje redactado (es decir, no es 'pendiente'), enviamos el correo
        if mensaje:
            try:
                send_mail(
                    subject=asunto,
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[postulacion.candidato.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar correo al candidato: {e}")
        # ====================================================================
        
    return redirect('jobs:ver_postulantes', id=postulacion.oferta.id)

        # ====================================================================
        # para ocultar las ofertas laborales en el empleador
        # ====================================================================

@login_required
def toggle_estado_oferta(request, oferta_id):
    # Usamos 'autor' porque así lo llamaste en tu modelo
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id, autor=request.user)
    
    if request.method == 'POST':
        oferta.activa = not oferta.activa
        oferta.save()
        
    # Cambia 'mis_ofertas' por el nombre de la vista donde el empleador ve sus publicaciones
    # Te devuelve a la página anterior. Si por algún motivo falla, te manda a tu dashboard por defecto.
    return redirect(request.META.get('HTTP_REFERER', '/accounts/dashboard/'))

        # ====================================================================
        # para que el candidato pueda quitar su postulacion a la oferta de trabajo
        # ====================================================================

@login_required
def despostular_a_oferta(request, id):
    oferta = get_object_or_404(OfertaLaboral, id=id)
    
    if request.method == 'POST':
        postulacion = Postulacion.objects.filter(oferta=oferta, candidato=request.user)
        
        if postulacion.exists():
            postulacion.delete()  # Elimina el registro de la postulación
            messages.success(request, 'Has retirado tu postulación con éxito.')
        else:
            messages.error(request, 'No estás postulado a esta oferta.')
            
    return redirect(request.META.get('HTTP_REFERER', 'jobs:lista_ofertas'))

        # ====================================================================
        # funcion para recibir un archivo
        # ====================================================================

