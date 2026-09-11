from django.contrib import admin
from django.urls import path
from chat import views

# Espacio de nombres de la aplicación
app_name = 'mensajes'

urlpatterns = [
    # Dashboard principal de comunicación
    path('admin/', admin.site.urls),

    path('', views.dashboard_principal, name='Inicio'),

    # Módulo 1: Comunicación Asíncrona
    path('chat_privado_individual/', views.chat_privado_individual, name='chat privado'),
    path('sala_canal_grupal/', views.sala_canal_grupal, name='grupo'),

    # Módulo 2: Retroalimentación y Escucha Activa

    path('retroalimentacion/nueva/', views.acuse_escucha_activa, name='registrar_retroalimentacion'),
]