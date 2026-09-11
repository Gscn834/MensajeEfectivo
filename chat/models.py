"""
Módulo 'chat': Contiene las estructuras para la mensajería privada 1 a 1
y los canales grupales con clasificación explícita de contexto.
"""
from django.db import models
from dispositivos.models import Dispositivo

class CanalGrupal(models.Model):
    """
    Canales clasificados en contexto Formal o Informal
    para evitar interferencias comunicativas.
    """
    TIPOS_CONTEXTO = [
        ('FORMAL', 'Profesional / Trabajo / Proyecto'),
        ('INFORMAL', 'Social / Amigos / Familia'),
    ]

    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True, help_text="Propósito claro del canal")
    tipo_contexto = models.CharField(max_length=10, choices=TIPOS_CONTEXTO, default='FORMAL')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.tipo_contexto}] {self.nombre}"


class MensajeGrupal(models.Model):
    """Mensajes enviados dentro de un canal público o comunitario."""
    canal = models.ForeignKey(CanalGrupal, on_delete=models.CASCADE, related_name='mensajes')
    emisor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha_envio']


class ConversacionPrivada(models.Model):
    """
    Representa una sala de chat privada y directa entre exactamente dos dispositivos.
    """
    dispositivo_1 = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='chats_iniciados')
    dispositivo_2 = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='chats_recibidos')
    fecha_inicio = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dispositivo_1', 'dispositivo_2')

    def __str__(self):
        return f"Chat Privado: {self.dispositivo_1.nombre_asignado} <-> {self.dispositivo_2.nombre_asignado}"


class MensajePrivado(models.Model):
    """Mensajes 1 a 1 intercambiados en una conversación privada."""
    conversacion = models.ForeignKey(ConversacionPrivada, on_delete=models.CASCADE, related_name='mensajes')
    emisor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha_envio']