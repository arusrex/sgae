from .models import Turma, AtribuicaoProfessor, Movimentacoes, FrequenciaProfessores
from core.models import Auditoria
from cadastros.models import Aluno, Sala, Professor
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages

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
        try:
            auditoria=Auditoria(
                acao='Exclusão de movimentação',
                criado_por=user,
                info=f'{movimentacao.aluno} excluída com êxito'
            )
            auditoria.save()
            movimentacao.delete()

            messages.success(request, 'Movimentação excluída com sucesso')

            return redirect('movimentacoes:movimentacoes')
        
        except Exception as e:
            print(f'Erro ao excluir movimentação: {e}')

            messages.error(request, 'Erro ao excluir movimentação, consulte o administrador')

    return redirect('movimentacoes:movimentacoes')

@login_required
def matricula(request):
    user = request.user.get_full_name()
    salas = Sala.objects.all().order_by('nome')
    total_alunos = Aluno.objects.exclude(turmas__isnull=False)

    if request.method == 'POST':
        try:
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

            messages.success(request, 'Matrícula realizada com sucesso')

            return redirect('movimentacoes:matricula')
        
        except Exception as e:
            print(f'Erro ao realizar matrícula: {e}')

            messages.error(request, 'Erro ao realizar matrícula, consulte o administrador')

            return redirect('movimentacoes:matricula')
     
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
        try:
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

            messages.success(request, 'Remanejamento realizado com sucesso')

            return redirect('movimentacoes:remanejamento')
        
        except Exception as e:
            print(f'Erro ao realizar remanejamento: {e}')

            messages.error(request, 'Erro ao realizar remanejamento, consulte o administrador')

            return redirect('movimentacoes:remanejamento')

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
        try:
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

            messages.success(request, 'Transferência realizada com sucesso')

            return redirect('movimentacoes:transferencia')
        
        except Exception as e:
            print(f'Erro ao realizar transferência')

            messages.error(request, 'Erro ao realizar transferência, consulte o administrador')

            return redirect('movimentacoes:transferencia')

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
    atribuicoes = AtribuicaoProfessor.objects.all()

    if request.method == 'POST':
        try:
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

            messages.success(request, 'Atribuição realizada com sucesso')

            return redirect('movimentacoes:atribuicoes')
        
        except Exception as e:
            print(f'Erro ao atribuir sala ao professor')

            messages.error(request, 'Erro ao atribuir sala ao professor, consulte o administrador')

            return redirect('movimentacoes:atribuicoes')

    context = {
        'atribuicoes': atribuicoes,
        'professores': professores,
        'salas': salas,
    }

    return render(request, 'atribuicao_professor.html', context)

@login_required
def excluir_atribuicoes(request, pk):
    user = request.user.get_full_name()
    atribuicao = get_object_or_404(AtribuicaoProfessor, pk=pk)

    if atribuicao:
        try:
            auditoria = Auditoria(
                acao=f'Exclusão de atribuição',
                criado_por=user,
                info=f'Atribuição do {atribuicao.professor} da sala {atribuicao.sala} excluída'
            )
            auditoria.save()
            atribuicao.delete()

            messages.warning(request, 'Atribuição excluída com sucesso')

            return redirect('movimentacoes:atribuicoes')

        except Exception as e:
            print(f'Erro ao excluir atribuição')

            messages.error(request, 'Erro ao excluir atribuição')

    return redirect('movimentacoes:atribuicoes')

@login_required
def faltas_professor(request, pk=None):
    TIPOS = [
        ('abonada', 'Abonada'),
        ('justificada', 'Justificada'),
        ('injustificada', 'Injustificada'),
        ('falta-aula', 'Falta-Aula'),
        ('ferias', 'Férias'),
        ('licenca-remunerada', 'Licença Remunerada'),
        ('licenca-premio', 'Licença Prêmio'),
        ('licenca-maternidade', 'Licença Maternidade'),
        ('licenca-paternidade', 'Licença Paternidade'),
        ('licenca-saude', 'Licença Saúde'),
        ('licenca-sem-vencimentos', 'Licença sem Vencimentos'),
        ('gala', 'Gala'),
        ('nojo', 'Nojo'),
        ('acidente-de-trabalho', 'Acidente de Trabalho'),
        ('doacao-de-sangue', 'Doação de Sangue'),
        ('ol', 'Serviço Obrigatório por LEI'),
        ('recesso-escolar', 'Recesso Escolar'),
    ]

    PERIODOS = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('manha-tarde', 'Manhã e Tarde'),
    ]

    user = request.user.get_full_name()
    professores = Professor.objects.all()
    faltas = FrequenciaProfessores.objects.all().order_by('professor')

    if request.method == "POST":
        try:
            professor = get_object_or_404(Professor, pk=request.POST.get('professor'))
            data_inicial = request.POST.get('data_inicial')
            data_final = request.POST.get('data_final')
            quantidade = request.POST.get('quantidade')
            periodo = request.POST.get('periodo')
            tipo = request.POST.get('tipo')

            falta = FrequenciaProfessores(
                professor=professor,
                data_inicial=data_inicial,
                data_final=data_final,
                quantidade=quantidade,
                periodo=periodo,
                tipo=tipo,
            )

            auditoria = Auditoria(
                acao=f'Falta de professor(a)',
                criado_por=user,
                info=f'Falta {tipo} para {professor}'
            )

            falta.save()
            auditoria.save()

            messages.success(request, 'Falta de professor(a) registrada com sucesso')
        
            return redirect('movimentacoes:faltas-professor')
        
        except Exception as e:
            print(f'Erro ao registrar falta de professor(a)')

            messages.error(request, 'Erro ao registrar falta de professor(a)')

            return redirect('movimentacoes:faltas-professor')

    context = {
        'professores': professores,
        'faltas': faltas,
        'tipos': TIPOS,
        'periodos': PERIODOS
    }

    return render(request, 'faltas_professor.html', context)

@login_required
def excluir_faltas_professor(request, pk):
    user = request.user.get_full_name()
    falta = get_object_or_404(FrequenciaProfessores, pk=pk)

    if falta:
        try:
            auditoria = Auditoria(
                acao=f'Exclusão de falta de professor',
                criado_por=user,
                info=f'Falta de {falta.data_inicial} do {falta.professor} excluída'
            )
            auditoria.save()
            falta.delete()

            messages.success(request, 'Falta excluída com sucesso')

            return redirect('movimentacoes:faltas-professor')


        except Exception as e:
            print(f'Erro ao excluir falta de professor: {e}')

            messages.error(request, 'Erro ao excluir falta de professor(a), consulte o administrador')

    return redirect('movimentacoes:faltas-professor')


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
        .order_by('-ano')
    )

    context = {
        'turmas': salas,
    }

    return render(request, 'turmas.html', context)

@login_required
def ficha_turma(request, pk):
    alunos_turma = Sala.objects.get(pk=pk).turmas.all() # type: ignore

    context = {
        'alunos_turma': alunos_turma,
    }

    return render(request, 'ficha_turma.html', context)

@login_required
def excluir_turma(request, pk):
    user = request.user.get_full_name()
    turma = get_object_or_404(Turma, pk=pk)

    if turma:
        try:
            auditoria = Auditoria(
                acao='Exclusão de aluno da turma',
                criado_por=user,
                info=f'{turma} foi excluído'
            )
            auditoria.save()
            turma.delete()

            messages.success(request, 'Turma excluída com sucesso')

            return redirect('movimentacoes:turmas')

        except Exception as e:
            print(f'Erro ao excluir turma: {e}')

            messages.error(request, 'Erro ao excluir turma, consulte o administrador')
    
    return redirect('movimentacoes:turmas')
