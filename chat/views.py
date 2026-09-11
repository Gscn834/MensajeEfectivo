"""
Controladores principales para la gestión del flujo de mensajes,
identificación de cookies UUID y procesamiento de retroalimentación.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from dispositivos.models import Dispositivo
from chat.models import CanalGrupal, MensajeGrupal, ConversacionPrivada, MensajePrivado
from evaluacion.models import EscuchaActiva, RetroalimentacionConstructiva
import uuid


def obtener_o_registrar_dispositivo(request):
    """
    Función auxiliar que extrae el UUID del dispositivo desde la cookie del navegador
    o genera un nuevo identificador si es la primera visita.
    """
    uuid_cookie = request.COOKIES.get('dispositivo_uuid')

    if not uuid_cookie:
        uuid_cookie = str(uuid.uuid4())
        nombre_defecto = f"Dispositivo-{uuid_cookie[:6]}"
    else:
        nombre_defecto = f"Dispositivo-{uuid_cookie[:6]}"

    ip_cliente = request.META.get('REMOTE_ADDR', '127.0.0.1')

    dispositivo, creado = Dispositivo.objects.get_or_create(
        uuid_dispositivo=uuid_cookie,
        defaults={'nombre_asignado': nombre_defecto, 'direccion_ip': ip_cliente}
    )
    return dispositivo, uuid_cookie


def dashboard_principal(request):
    """Panel general que lista los canales de chat y los dispositivos en la red local."""
    dispositivo_actual, uuid_cookie = obtener_o_registrar_dispositivo(request)

    if request.method == 'POST' and 'actualizar_nombre' in request.POST:
        nuevo_nombre = request.POST.get('nombre_asignado', '').strip()
        if nuevo_nombre:
            dispositivo_actual.nombre_asignado = nuevo_nombre
            dispositivo_actual.save()

    canales_formales = CanalGrupal.objects.filter(tipo_contexto='FORMAL')
    canales_informales = CanalGrupal.objects.filter(tipo_contexto='INFORMAL')
    otros_dispositivos = Dispositivo.objects.exclude(id=dispositivo_actual.id)

    response = render(request, 'dashboard.html', {
        'dispositivo_actual': dispositivo_actual,
        'canales_formales': canales_formales,
        'canales_informales': canales_informales,
        'otros_dispositivos': otros_dispositivos,
    })

    # Persistir identificador unívoco de dispositivo por 1 año
    response.set_cookie('dispositivo_uuid', uuid_cookie, max_age=31536000)
    return response


def sala_canal_grupal(request, canal_id):
    """Sostiene la comunicación dentro de un canal comunitario especifico."""
    dispositivo_actual, _ = obtener_o_registrar_dispositivo(request)
    canal = get_object_or_404(CanalGrupal, id=canal_id)

    if request.method == 'POST':
        texto_mensaje = request.POST.get('contenido', '').strip()
        if texto_mensaje:
            MensajeGrupal.objects.create(
                canal=canal,
                emisor=dispositivo_actual,
                contenido=texto_mensaje
            )
            return redirect('sala_canal_grupal', canal_id=canal.id)

    mensajes = canal.mensajes.all()
    return render(request, 'sala_canal.html', {
        'canal': canal,
        'mensajes': mensajes,
        'dispositivo_actual': dispositivo_actual
    })


def chat_privado_individual(request, dispositivo_destino_id):
    """
    Gestiona la conversación 1 a 1 entre el dispositivo emisor y otro dispositivo destino.
    """
    dispositivo_emisor, _ = obtener_o_registrar_dispositivo(request)
    dispositivo_destino = get_object_or_404(Dispositivo, id=dispositivo_destino_id)

    # Buscar o crear conversación bidireccional única
    conversacion = ConversacionPrivada.objects.filter(
        (Q(dispositivo_1=dispositivo_emisor) & Q(dispositivo_2=dispositivo_destino)) |
        (Q(dispositivo_1=dispositivo_destino) & Q(dispositivo_2=dispositivo_emisor))
    ).first()

    if not conversacion:
        conversacion = ConversacionPrivada.objects.create(
            dispositivo_1=dispositivo_emisor,
            dispositivo_2=dispositivo_destino
        )

    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            MensajePrivado.objects.create(
                conversacion=conversacion,
                emisor=dispositivo_emisor,
                contenido=contenido
            )
            return redirect('chat_privado_individual', dispositivo_destino_id=dispositivo_destino.id)

    mensajes = conversacion.mensajes.all()
    return render(request, 'chat_privado.html', {
        'conversacion': conversacion,
        'dispositivo_emisor': dispositivo_emisor,
        'dispositivo_destino': dispositivo_destino,
        'mensajes': mensajes
    })


def acuse_escucha_activa(request, mensaje_id):
    """Registra la confirmación de lectura analítica de un mensaje."""
    dispositivo_actual, _ = obtener_o_registrar_dispositivo(request)
    mensaje = get_object_or_404(MensajeGrupal, id=mensaje_id)

    EscuchaActiva.objects.get_or_create(
        mensaje=mensaje,
        dispositivo_receptor=dispositivo_actual
    )
    return redirect('sala_canal_grupal', canal_id=mensaje.canal.id)