from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Evento
from rest_framework import generics
from .serializers import *
import requests


def eventos_view(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos.html', {'eventos': eventos})


def eventos_add(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('eventos_view')
    else:
        form = EventoForm()
    return render(request, 'eventos_form.html', {'form': form})


def eventos_change(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, f'evento "{evento.nombre_evento}" editado correctamente')
            return redirect('eventos_view')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos_form.html', {'form': form})


def ponencias_view(request):
    ponencias = Ponencia.objects.all()
    return render(request, 'ponencias.html', {'ponencias': ponencias})


def ponencias_add_1(request):
    if request.method == 'POST':
        form = PonenciaForm1(request.POST, request.FILES)
        if form.is_valid():
            ponencia = form.save()
            ponencia_id = ponencia.id
            print()
            return redirect(f'/ponencias/add/{ponencia_id}/')
    else:
        form = PonenciaForm1()
    return render(request, 'ponencias_form_1.html', {'form': form})


def ponencias_add_2(request, ponencia_id):
    ponencia = get_object_or_404(Ponencia, pk=ponencia_id)
    if request.method == 'POST':
        form = PonenciaForm2(request.POST, request.FILES, instance=ponencia)
        if form.is_valid():
            form.save()
            return redirect('ponencias_view')
    else:
        form = PonenciaForm2(instance=ponencia)
    return render(request, 'ponencias_form_2.html', {'form': form, 'ponencia': ponencia})


def ponencias_ia_summary(request, ponencia_id):
    api_url = 'https://summary-and-text-to-speech.onrender.com/summarize/'
    ponencia = get_object_or_404(Ponencia, pk=ponencia_id)
    file_path = ponencia.documento_original.path
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(api_url, files=files)
        if response.status_code == 200:
            summary_content = response.content
            summary_dir = os.path.join(settings.MEDIA_ROOT, 'ponencias/summary/') 
            os.makedirs(summary_dir, exist_ok=True)
            summary_file_path = os.path.join(summary_dir, f'{ponencia.id}_summary.docx')
            with open(summary_file_path, 'wb') as summary_file:
                summary_file.write(summary_content)
            ponencia.summary = summary_file_path
            ponencia.save()
            messages.success(request, f'Summary saved successfully!')
        else:
            messages.error(request, f'Summary not saved successfully!')
    return redirect(f'/ponencias/add/{ponencia_id}/')


class EventoListCreateApi(generics.ListCreateAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    # def perform_create(self, serializer):
    #     serializer.save(updated_by=str(self.request.user))


class EventoRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(updated_by=str(self.request.user))


class PonenciaListCreateApi(generics.ListCreateAPIView):
    queryset = Ponencia.objects.all()
    serializer_class = PonenciaSerializer

    # def perform_create(self, serializer):
    #     serializer.save(updated_by=str(self.request.user))


class PonenciaRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ponencia.objects.all()
    serializer_class = PonenciaSerializer
    lookup_field = 'pk'

    # def perform_update(self, serializer):
    #     serializer.save(updated_by=str(self.request.user))


class PonenciaByEvento(generics.ListAPIView):
    serializer_class = PonenciaSerializer

    def get_queryset(self):
        evento_id = self.kwargs['evento_id']
        return Ponencia.objects.filter(evento_id=evento_id)
