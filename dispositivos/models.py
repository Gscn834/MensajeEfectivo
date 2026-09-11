
"""
Módulo 'dispositivos': Gestiona el identificador único físico/lógico (UUID)
de cada equipo o navegador que accede a la aplicación en la red local.
"""
from django.db import models
import uuid

class Dispositivo(models.Model):
    """
    Modelo que representa un nodo o terminal en la red local.
    Permite asociar un identificador persistente sin necesidad de login complejo.
    """
    uuid_dispositivo = models.CharField(
        max_length=64,
        unique=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Token unívoco asignado mediante cookie al dispositivo/navegador"
    )
    nombre_asignado = models.CharField(
        max_length=100,
        help_text="Nombre identificativo del equipo (Ej. 'Laptop Omar', 'PC Oficina 2')"
    )
    direccion_ip = models.GenericIPAddressField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dispositivo Local"
        verbose_name_plural = "Dispositivos Locales"
        ordering = ['-ultimo_acceso']

    def __str__(self):
        return f"{self.nombre_asignado} ({self.uuid_dispositivo[:8]})"