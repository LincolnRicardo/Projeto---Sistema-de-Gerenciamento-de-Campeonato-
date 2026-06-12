from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, F
from django.db import models
from django.contrib import messages
from partidas.models import Partida, Evento
from times.models import Time
from jogadores.models import Jogador
from campeonatos.models import Campeonato


def dashboard(request):
    # Totais gerais
    total_partidas = Partida.objects.filter(status='EN').count()
    total_gols = Evento.objects.filter(tipo='GOL').count()
    total_times = Time.objects.count()
    total_jogadores = Jogador.objects.count()

    # Últimas partidas realizadas
    ultimas_partidas = Partida.objects.filter(status='EN').order_by('-data')[:5]

    # Partidas ao vivo
    ao_vivo = Partida.objects.filter(status='AO')

    # Artilheiros
    artilheiros = Jogador.objects.annotate(
        gols=Count('eventos', filter=Q(eventos__tipo='GOL'))
    ).filter(gols__gt=0).order_by('-gols')[:10]

    # Cartões
    cartoes_amarelos = Evento.objects.filter(tipo='CAR').count()
    cartoes_vermelhos = Evento.objects.filter(tipo='VER').count()

    # Classificação
    times = Time.objects.all()
    classificacao = []
    for time in times:
        vitorias = Partida.objects.filter(status='EN').filter(
            Q(time_casa=time, gols_casa__gt=F('gols_visitante')) |
            Q(time_visitante=time, gols_visitante__gt=F('gols_casa'))
        ).count()
        empates = Partida.objects.filter(
            status='EN', gols_casa=F('gols_visitante')
        ).filter(Q(time_casa=time) | Q(time_visitante=time)).count()
        derrotas = Partida.objects.filter(status='EN').filter(
            Q(time_casa=time, gols_casa__lt=F('gols_visitante')) |
            Q(time_visitante=time, gols_visitante__lt=F('gols_casa'))
        ).count()
        jogos = vitorias + empates + derrotas
        pontos = (vitorias * 3) + empates
        
        classificacao.append({
                'time': time,
                'jogos': jogos,
                'vitorias': vitorias,
                'empates': empates,
                'derrotas': derrotas,
                'pontos': pontos,
            })
    classificacao.sort(key=lambda x: (x['pontos'], x['vitorias']), reverse=True)

    # Dados para o formulário
    todos_times = Time.objects.all()
    campeonatos = Campeonato.objects.all()
    todas_partidas = Partida.objects.exclude(status='EN').order_by('-data')
    todos_jogadores = Jogador.objects.all()

    context = {
        'total_partidas': total_partidas,
        'total_gols': total_gols,
        'total_times': total_times,
        'total_jogadores': total_jogadores,
        'ultimas_partidas': ultimas_partidas,
        'ao_vivo': ao_vivo,
        'artilheiros': artilheiros,
        'cartoes_amarelos': cartoes_amarelos,
        'cartoes_vermelhos': cartoes_vermelhos,
        'classificacao': classificacao,
        'todos_times': todos_times,
        'campeonatos': campeonatos,
        'todas_partidas': todas_partidas,
        'todos_jogadores': todos_jogadores,
    }
    return render(request, 'dashboard.html', context)


def nova_partida(request):
    if request.method == 'POST':
        campeonato_id = request.POST.get('campeonato')
        time_casa_id = request.POST.get('time_casa')
        time_visitante_id = request.POST.get('time_visitante')
        data = request.POST.get('data')
        Partida.objects.create(
            campeonato_id=campeonato_id,
            time_casa_id=time_casa_id,
            time_visitante_id=time_visitante_id,
            data=data,
            status='AG'
        )
        messages.success(request, 'Partida criada com sucesso!')
    return redirect('/?aba=gerenciar')


def alterar_status(request, partida_id):
    if request.method == 'POST':
        partida = get_object_or_404(Partida, pk=partida_id)
        novo_status = request.POST.get('status')
        partida.status = novo_status
        partida.save()
        messages.success(request, 'Status atualizado!')
    return redirect('/?aba=gerenciar')


def detalhe_partida(request, pk):
    partida = get_object_or_404(Partida, pk=pk)

    return render(
        request,
        'detalhe_partida.html',
        {
            'partida': partida,
            'eventos': partida.eventos.all()
        }
    )

def registrar_evento(request, partida_id):
    if request.method == 'POST':
        partida = get_object_or_404(Partida, pk=partida_id)
        tipo = request.POST.get('tipo')
        minuto = int(request.POST.get('minuto', 0))
        descricao = request.POST.get('descricao', '')
        jogador_id = request.POST.get('jogador')

        evento = Evento(
            partida=partida,
            tipo=tipo,
            minuto=minuto,
            descricao=descricao,
        )
        if jogador_id:
            evento.jogador_id = jogador_id
        evento.save()

        # Atualiza placar se for gol
        if tipo == 'GOL' and jogador_id:
            jogador = Jogador.objects.get(pk=jogador_id)
            if jogador.time == partida.time_casa:
                partida.gols_casa += 1
            else:
                partida.gols_visitante += 1
            partida.save()

        messages.success(request, 'Evento registrado!')
    return redirect('/?aba=gerenciar')