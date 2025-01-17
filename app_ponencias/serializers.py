from rest_framework import serializers
from app_ponencias.models import *
# from django.contrib.auth.models import User


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ["id", "nombre_evento", "fecha", "lugar"]


class PonenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponencia
        fields = ['evento', 'nombre_ponencia', 'autor', 'documento_original', 'audio_file', 'summary']

