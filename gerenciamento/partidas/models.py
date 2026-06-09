from django.db import models
from times.models import Time
from campeonatos.models import Campeonato

class Partida(models.Model):
    STATUS = [
        ('AG', 'Aguardando'),
        ('AO', 'Ao Vivo'),
        ('EN', 'Encerrada'),
    ]
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE, related_name='partidas')
    time_casa = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='partidas_casa')
    time_visitante = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='partidas_visitante')
    data = models.DateTimeField()
    status = models.CharField(max_length=2, choices=STATUS, default='AG')
    gols_casa = models.IntegerField(default=0)
    gols_visitante = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.time_casa} x {self.time_visitante}" #mostando os times da partida


class Evento(models.Model):
    TIPOS = [
        ('GOL', '⚽ Gol'),
        ('CAR', '🟨 Cartão Amarelo'),
        ('VER', '🟥 Cartão Vermelho'),
        ('SUB', '🔄 Substituição'),
    ]
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, related_name='eventos')
    tipo = models.CharField(max_length=3, choices=TIPOS)
    minuto = models.IntegerField()
    descricao = models.CharField(max_length=200)
    criado_em = models.DateTimeField(auto_now_add=True)
    jogador = models.ForeignKey('jogadores.Jogador', on_delete=models.SET_NULL, null=True, blank=True, related_name='eventos')

    class Meta:
        ordering = ['minuto'] #utilizei para ficar em ordem cronologica cada evento do jogo

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.minuto}' ({self.partida})"  #mostando o que aconteceu no jogo, minutos e qual partida