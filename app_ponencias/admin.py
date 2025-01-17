from django.contrib import admin
from .models import *


# @admin.register(AudioTranslation)
# class AudioTranslationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'file', 'audio_file')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_evento', 'fecha')


@admin.register(Ponencia)
class PonenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'evento', 'nombre_ponencia', 'autor', 'documento_original', 'audio_file', 'summary')