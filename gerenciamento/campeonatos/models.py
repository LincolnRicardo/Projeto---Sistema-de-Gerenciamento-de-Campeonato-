from django.db import models
from times.models import Time

class Campeonato(models.Model):
    nome = models.CharField(max_length=100)
    ano= models.IntegerField()
    times  = models.ManyToManyField(Time, related_name='campeonatos', blank=True)

    def __str__(self):
        return f"{self.nome} {self.ano}"
    


