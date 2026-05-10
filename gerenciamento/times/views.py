from django.views.generic import ListView, DetailView
from .models import Time

class TimeListView(ListView):
    model = Time
    template_name = 'times/lista.html'
    context_object_name = 'times'

class TimeDetailView(DetailView):
    model = Time
    template_name = 'times/detalhe.html'
    context_object_name = 'time'