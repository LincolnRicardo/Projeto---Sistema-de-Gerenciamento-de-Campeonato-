from django.db import models
from times.models import Time

class Jogador (models.Model):
    POSICOES = [
        ('GOL', 'Goleiro'),
        ('ZAG', 'Zagueiro'),
        ('LAT', 'Lateral'),
        ('VOL', 'Volante'),
        ('MEI', 'Meia'),
        ('ATA', 'Atacante'),
    ]
    nome = models.CharField(max_length=55)
    numero= models.IntegerField()
    posicao = models.CharField(max_length=3, choices=POSICOES)
    time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='jogadores')
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome}({self.time.nome})"


