from django.db import models
from docx import Document
from gtts import gTTS
import os
from django.conf import settings


class Evento(models.Model):
    nombre_evento = models.CharField('Nombre Evento', max_length=100)
    fecha = models.DateField(auto_now_add=False, auto_now=False)
    lugar = models.CharField('Lugar', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_evento


def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

class Ponencia(models.Model):
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE)
    nombre_ponencia = models.CharField('Nombre Ponencia', max_length=100)
    autor = models.CharField('Autor', max_length=100)
    documento_original = models.FileField(upload_to='ponencias/originales/')
    audio_file = models.FileField(upload_to='ponencias/audio/', blank=True, null=True)
    summary = models.FileField(upload_to='ponencias/summary/', blank=True, null=True)

    def __str__(self):
        if self.nombre_ponencia:
            return self.nombre_ponencia
        else:
            return str(self.id)

    def translate_to_audio(self):
        file_path = os.path.join(settings.MEDIA_ROOT, self.summary.path)
        if file_path.endswith('.docx'):
            text = read_docx(file_path)

        tts = gTTS(text=text, lang='es')
        # audio_path = os.path.join(os.path.dirname(file_path), f'{self.pk}_audio.mp3')
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'ponencias/audio/') 
        os.makedirs(audio_dir, exist_ok=True)
        audio_file_path = os.path.join(audio_dir, f'{self.pk}_audio.mp3')
        # audio_path = settings.MEDIA_ROOT + '/ponencias/audio/' + f'{self.pk}_audio.mp3'
        tts.save(audio_file_path)
        # self.audio_file.name = '/ponencias/audio/' + f'{self.pk}_audio.mp3'  # Ensure the name is correctly set
        self.audio_file = audio_file_path
        # self.audio_file.name = '/ponencias/audio/' + f'{self.pk}_audio.mp3'
        super(Ponencia, self).save(update_fields=['audio_file'])

    def save(self, *args, **kwargs):
        super(Ponencia, self).save(*args, **kwargs)
        if self.summary and not self.audio_file:
            self.translate_to_audio()
            super(Ponencia, self).save(update_fields=['audio_file'])
