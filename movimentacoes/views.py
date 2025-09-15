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
def matricula(request):
    user = request.user.get_full_name()
    salas = Sala.objects.all().order_by('nome')
    total_alunos = Aluno.objects.exclude(turmas__isnull=False)

    if request.method == 'POST':
        aluno = request.POST.get('aluno')
        data = request.POST.get('data')
        origem = request.POST.get('origem')
        destino = request.POST.get('destino')

        turma = Turma(
            sala=get_object_or_404(Sala, pk=destino),
            aluno=get_object_or_404(Aluno, pk=aluno),
            numero_aluno=Turma.objects.filter(sala__pk=destino).count() + 1,
            status='Ativo',
        )

        movimentacao = Movimentacoes(
            aluno=get_object_or_404(Aluno, pk=aluno),
            origem_input=origem,
            destino=get_object_or_404(Sala, pk=destino),
            tipo='Matrícula',
            data=data
        )

        auditoria = Auditoria(
            acao=f'Nova matrícula',
            criado_por=user,
            info=f'{get_object_or_404(Aluno,pk=aluno)} matriculado no {get_object_or_404(Sala, pk=destino)}'
        )

        turma.save()
        movimentacao.save()
        auditoria.save()
     
    context = {
        'matricula': True,
        'total_alunos': total_alunos,
        'salas': salas
    }
    
    return render(request, 'form-movimentacao.html', context)

@login_required
def remanejamento(request, pk=None):
    user = request.user.get_full_name()
    salas = Sala.objects.filter(ano=datetime.date.today().year)
    total_alunos = Aluno.objects.exclude(turmas__isnull=True)

    if request.method == 'POST':
        aluno = request.POST.get('aluno')
        data = request.POST.get('data')
        origem = request.POST.get('origem')
        destino = request.POST.get('destino')

        movimentacao = Movimentacoes(
            aluno=get_object_or_404(Aluno, pk=aluno),
            origem=get_object_or_404(Sala, pk=origem),
            destino=get_object_or_404(Sala, pk=destino),
            tipo='Remanejamento',
            data=data
        )

        turma = get_object_or_404(Turma, aluno=aluno)
        turma.status = 'Remanejado'

        nova_turma = Turma(
            sala=get_object_or_404(Sala, pk=destino),
            aluno=get_object_or_404(Aluno, pk=aluno),
            numero_aluno=Turma.objects.filter(sala=destino).count() + 1,
            status='Ativo'
        )

        movimentacao.save()
        turma.save()
        nova_turma.save()

    context = {
        'remanejamento': True,
        'total_alunos': total_alunos,
        'salas': salas,
    }

    return render(request, 'form-movimentacao.html', context)

@login_required
def transferencia(request, pk=None):
    user = request.user.get_full_name()
    salas = Sala.objects.filter(ano=datetime.date.today().year)
    total_alunos = Aluno.objects.exclude(turmas__isnull=True)

    context = {
        'transferencia': True,
        'total_alunos': total_alunos,
        'salas': salas,
    }

    return render(request, 'form-movimentacao.html', context)

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
