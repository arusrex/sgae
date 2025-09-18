from .models import Turma, AtribuicaoProfessor, Movimentacoes, FrequenciaProfessores
from core.models import Auditoria
from cadastros.models import Aluno, Sala, Professor
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def movimentacoes(request):
    user = request.user.get_full_name()
    movimentacoes = Movimentacoes.objects.all().order_by('data')

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
    total_alunos = Aluno.objects.filter(turmas__status='Ativo')

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

        turma = Turma.objects.filter(aluno=aluno, status='Ativo').first()
        if turma:
            turma.status = 'Remanejado'
            turma.save()

        nova_turma = Turma(
            sala=get_object_or_404(Sala, pk=destino),
            aluno=get_object_or_404(Aluno, pk=aluno),
            numero_aluno=Turma.objects.filter(sala=destino).count() + 1,
            status='Ativo'
        )

        auditoria = Auditoria(
            acao=f'Remanejamento de aluno(a)',
            criado_por=f'{user}',
            info=f'{turma.aluno if turma else 'Sem dados'} remanejado(a) do {movimentacao.origem} para {movimentacao.destino}'
        )

        movimentacao.save()
        nova_turma.save()
        auditoria.save()

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
    total_alunos = Aluno.objects.filter(turmas__status='Ativo')

    if request.method == 'POST':
        aluno = request.POST.get('aluno')
        data = request.POST.get('data')
        origem = request.POST.get('origem')
        destino = request.POST.get('destino')

        movimentacao = Movimentacoes(
            aluno=get_object_or_404(Aluno, pk=aluno),
            origem=get_object_or_404(Sala, pk=origem),
            destino_input=destino,
            tipo='Transferência',
            data=data
        )

        turma = Turma.objects.filter(aluno=aluno, status='Ativo').first()
        if turma:
            turma.status = 'Transferido'
            turma.save()

        auditoria = Auditoria(
            acao=f'Transferência de aluno(a)',
            criado_por=user,
            info=f'{turma.aluno if turma else 'Sem dados'} tranferido para {destino}'
        )

        movimentacao.save()
        auditoria.save()

    context = {
        'transferencia': True,
        'total_alunos': total_alunos,
        'salas': salas,
    }

    return render(request, 'form-movimentacao.html', context)

@login_required
def atribuicao_professor(request, pk=None):
    user = request.user.get_full_name()
    professores = Professor.objects.all()
    salas = Sala.objects.all()

    if request.method == 'POST':
        professor = get_object_or_404(Professor, pk=request.POST.get('professor'))
        sala = get_object_or_404(Sala, pk=request.POST.get('sala'))

        atribuicao = AtribuicaoProfessor(
            professor=professor,
            sala=sala,
        )

        auditoria = Auditoria(
            acao=f'Atribuição de professor(a)',
            criado_por=user,
            info=f'{professor} atribuído a sala {sala} com sucesso'
        )

        atribuicao.save()
        auditoria.save()

    context = {
        'professores': professores,
        'salas': salas,
    }

    return render(request, 'atribuicao_professor.html', context)

@login_required
def faltas_professor(request, pk=None):
    professores = Professor.objects.all()
    faltas = FrequenciaProfessores.objects.all().order_by('professor')

    if request.method == "POST":
        professor = request.POST.get('professor')
        data_inicial = request.POST.get('data_inicial')
        data_final = request.POST.get('data_final')
        quantidade = request.POST.get('quantidade')
        periodo = request.POST.get('periodo')
        tipo = request.POST.get('tipo')
    
        print(f"{professor}\n{data_inicial}\n{data_final}\n{quantidade}\n{periodo}\n{tipo}")

    context = {
        'professores': professores,
        'faltas': faltas,
    }

    return render(request, 'faltas_professor.html', context)

@login_required
def turmas(request, pk=None):
    salas = (
        Sala.objects.all()
        .annotate(
            ativos=Count('turmas', Q(turmas__status="Ativo")),
            inativos=Count('turmas', Q(turmas__status="Inativo")),
            remanejados=Count('turmas', Q(turmas__status="Remanejado")),
            transferidos=Count('turmas', Q(turmas__status="Transferido")),
            concluidos=Count('turmas', Q(turmas__status="Concluído")),
            total=Count('turmas'),
        )
    )

    context = {
        'turmas': salas,
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
