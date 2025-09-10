from .models import Turma, AtribuicaoProfessor, Movimentacoes
from cadastros.models import Aluno, Sala
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def movimentacoes(request, pk=None):
    user = request.user.get_full_name()
    alunos = Aluno.objects.all().order_by('nome')
    salas = Sala.objects.filter(ano=datetime.date.today().year)
    movimentacoes = Movimentacoes.objects.all().order_by('-pk')

    if request.method == 'POST':

        tipo = request.POST.get('tipo')
        aluno = request.POST.get('aluno')
        data = request.POST.get('data')
        origem = request.POST.get('origem')
        destino = request.POST.get('destino')

        print(
            'Tipo:', tipo, f'\n',
            'Aluno:', aluno, f'\n',
            'Data:', data, f'\n',
            'Origem:', origem, f'\n',
            'Destino:', destino, f'\n',
        )

        if tipo == 'matricula':
            qtd_na_sala = Turma.objects.filter(sala=destino).count()
            numero_do_aluno = qtd_na_sala + 1
            movimentacao = Movimentacoes(
                tipo=tipo,
                aluno=get_object_or_404(Aluno, pk=aluno),
                data=data,
                origem_input=origem,
                destino=get_object_or_404(Sala, pk=destino),
            )

            adicionar_na_turma = Turma(
                sala=get_object_or_404(Sala, pk=destino),
                aluno=get_object_or_404(Aluno, pk=aluno),
                numero_aluno=numero_do_aluno,
                status='Ativo'
            )

            movimentacao.save()
            adicionar_na_turma.save()

        elif tipo == 'remanejamento':
            qtd_na_sala = Turma.objects.filter(sala=destino).count()
            numero_do_aluno = qtd_na_sala + 1
            movimentacao = Movimentacoes(
                tipo=tipo,
                aluno=get_object_or_404(Aluno, pk=aluno),
                data=data,
                origem=get_object_or_404(Sala, pk=origem),
                destino=get_object_or_404(Sala, pk=destino),
            )

            turma_antiga_aluno = Turma.objects.get(sala=origem, aluno=aluno)
            if turma_antiga_aluno:
                turma_antiga_aluno.status = 'Remanejado'
                turma_antiga_aluno.save()

            adicionar_na_turma = Turma(
                sala=get_object_or_404(Sala, pk=destino),
                aluno=get_object_or_404(Aluno, pk=aluno),
                numero_aluno=numero_do_aluno,
                status='Ativo'
            )

            movimentacao.save()
            adicionar_na_turma.save()

        elif tipo == 'transferencia':
            turma_antiga_aluno = Turma.objects.get(sala=origem, aluno=aluno)
            
            movimentacao = Movimentacoes(
                tipo=tipo,
                aluno=get_object_or_404(Aluno, pk=aluno),
                data=data,
                origem=get_object_or_404(Sala, pk=origem),
                destino_input=destino,
            )

            if turma_antiga_aluno:
                turma_antiga_aluno.status = 'Transferido'
                turma_antiga_aluno.save()

        return redirect('movimentacoes:movimentacoes')

    context = {
        'movimentacoes': movimentacoes,
        'tipos_movimentacao': Movimentacoes.TIPOS,
        'alunos_movimentacao': alunos,
        'salas_movimentacao': salas,
    }

    return render(request, 'movimentacoes.html', context)

@login_required
def atribuicao_professor(request, pk=None):

    return render(request, 'atribuicao_professor.html')

@login_required
def faltas_professor(request, pk=None):

    return render(request, 'faltas_professor.html')

@login_required
def turmas(request, pk=None):
    turmas = Turma.objects.all().order_by('sala')

    context = {
        'turmas': turmas,
    }

    return render(request, 'turmas.html', context)