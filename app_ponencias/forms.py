from django import forms
from .models import *


# class AudioTranslationForm(forms.ModelForm):
#     class Meta:
#         model = AudioTranslation
#         fields = ['file']


class EventoForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'), input_formats=['%Y-%m-%d'])

    class Meta:
        model = Evento
        fields = ['nombre_evento', 'fecha', 'lugar']


class PonenciaForm1(forms.ModelForm):

    class Meta:
        model = Ponencia
        fields = ['evento', 'nombre_ponencia', 'autor', 'documento_original']


class PonenciaForm2(forms.ModelForm):

    class Meta:
        model = Ponencia
        fields = ['summary']
