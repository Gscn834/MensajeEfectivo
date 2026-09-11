"""
Módulo 'evaluacion': Codifica conceptos de Comunicación Efectiva como 
Escucha Activa (confirmación analítica de lectura) y Retroalimentación Constructiva.
"""
from django.db import models
from dispositivos.models import Dispositivo
from chat.models import MensajeGrupal

class EscuchaActiva(models.Model):
    """
    Registra el acuse de recibo consciente de un receptor hacia un mensaje formal.
    Demuestra la técnica de verificación de recepción de la instrucción.
    """
    mensaje = models.ForeignKey(MensajeGrupal, on_delete=models.CASCADE, related_name='acuses_escucha')
    dispositivo_receptor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    fecha_confirmacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mensaje', 'dispositivo_receptor')
        verbose_name = "Confirmación de Escucha Activa"

    def __str__(self):
        return f"{self.dispositivo_receptor.nombre_asignado} entendió Msg #{self.mensaje.id}"


class RetroalimentacionConstructiva(models.Model):
    """
    Módulo para enviar evaluaciones o retroalimentación sobre la claridad
    de la comunicación dentro de un equipo o proyecto.
    """
    emisor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='retroalimentaciones_enviadas')
    receptor = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='retroalimentaciones_recibidas')
    aspectos_positivos = models.TextField(help_text="Qué se comunicó de forma clara y efectiva")
    puntos_mejora = models.TextField(help_text="Qué barreras o ruidos se detectaron")
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)