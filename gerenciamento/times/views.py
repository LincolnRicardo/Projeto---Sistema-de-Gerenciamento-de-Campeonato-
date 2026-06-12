from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Time
class TimeListView(ListView):
    model = Time
    template_name = 'times/lista.html'
    context_object_name = 'times'

class TimeDetailView(DetailView):
    model = Time
    template_name = 'times/detalhe.html'
    context_object_name = 'time'
class TimeCriarView(CreateView):
    model = Time
    fields = ['nome', 'cidade', 'estadio', 'tecnico', 'escudo']
    template_name = 'times/criar.html'
    success_url = reverse_lazy('times-lista')