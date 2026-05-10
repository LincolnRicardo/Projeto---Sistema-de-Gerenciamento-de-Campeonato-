from django.db import models

# Create your models here.
from django.db import models

class Time(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estadio= models.CharField(max_length=100)
    tecnico= models.CharField(max_length=100)
    data_fundacao= models.DateTimeField()

    def __str__(self):
        return self.nome
    