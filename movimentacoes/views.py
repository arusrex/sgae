from .models import Turma, AtribuicaoProfessor, Movimentacoes
from core.models import Auditoria
from cadastros.models import Aluno, Sala
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def movimentacoes(request):
    user = request.user.get_full_name()
    movimentacoes = Movimentacoes.objects.all().order_by('-pk')

    context = {
        'movimentacoes': movimentacoes,
    }

    return render(request, 'movimentacoes.html', context)

@login_required
def excluir_movimentacao(request, pk):
    user = request.user.get_full_name()
    movimentacao = get_object_or_404(Movimentacoes, pk=pk)

    if movimentacao:
        auditoria=Auditoria(
            acao='Exclusão de movimentação',
            criado_por=user,
            info=f'{movimentacao.aluno} excluída com êxito'
        )
        auditoria.save()
        movimentacao.delete()
    
    return redirect('movimentacoes:movimentacoes')

@login_required
def matricula(request, pk=None):
    user = request.user.get_full_name()
    alunos = Aluno.objects.all().order_by('nome')
    salas = Sala.objects.all().order_by('nome')
    alunos_matriculados = Turma.objects.select_related('aluno').all()
    alunos_sem_sala = Aluno.objects.exclude(turma__isnull=False)
     
    context = {
        'alunos_sem_sala': alunos_sem_sala,
        'salas': salas
    }
    
    return render(request, 'matricula.html', context)

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

@login_required
def excluir_turma(request, pk):
    user = request.user.get_full_name()
    turma = get_object_or_404(Turma, pk=pk)

    if turma:
        auditoria = Auditoria(
            acao='Exclusão de aluno da turma',
            criado_por=user,
            info=f'{turma} foi excluído'
        )
        auditoria.save()
        turma.delete()
    
    return redirect('movimentacoes:turmas')
