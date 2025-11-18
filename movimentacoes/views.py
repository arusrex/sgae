from .models import Turma, AtribuicaoProfessor, Movimentacoes, FrequenciaProfessores, FrequenciaFuncionarios
from core.models import Auditoria
from cadastros.models import Aluno, Sala, Professor, Funcionario
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime

TIPOS_FUNCIONARIOS = [
    ('justificada', 'Justificada'),
    ('injustificada', 'Injustificada'),
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

TIPOS_PROFESSOR = [
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

@login_required
def movimentacoes(request):
    user = request.user.get_full_name()
    movimentacoes = Movimentacoes.objects.all().order_by('-data', '-pk')

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
    salas = Sala.objects.all().order_by('serie', 'classe', 'periodo')
    total_alunos = Aluno.objects.exclude(turmas__status__in=["Ativo", "Remanejado", "Concluído"]).order_by('nome')

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
    salas = Sala.objects.filter(ano=datetime.date.today().year).order_by('serie', 'classe', 'periodo')
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
    salas = Sala.objects.filter(ano=datetime.date.today().year).order_by('serie')
    total_alunos = Aluno.objects.filter(turmas__status='Ativo').order_by('turmas__aluno')

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
    user = request.user.get_full_name()
    professores = Professor.objects.all().order_by('user__first_name')
    faltas = FrequenciaProfessores.objects.all().order_by('-pk')

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
        'tipos': TIPOS_PROFESSOR,
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
    user = request.user
    movimentacoes_turma = Turma.objects.all()
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
        .order_by('serie', 'classe', 'periodo', '-ano')
    )

    if pk:
        turma = get_object_or_404(Turma, pk=pk)

        if turma:
            messages.warning(request, 'Movimentação de turma excluída com sucesso')
            Auditoria.objects.create(acao='Exclusão na movimentação de turma',criado_por=user, info=f'{turma} excluída com sucesso')
            turma.delete()
            return redirect('movimentacoes:turmas')

    context = {
        'turmas': salas,
        'movimentacoes_turma': movimentacoes_turma,
    }

    return render(request, 'turmas.html', context)

@login_required
def ficha_turma(request, pk):
    alunos_turma = Sala.objects.get(pk=pk).turmas.all().order_by("numero_aluno") # type: ignore

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


@login_required
def faltas_funcionario(request, pk=None):
    user = request.user.get_full_name()
    funcionarios = Funcionario.objects.all()
    faltas = FrequenciaFuncionarios.objects.all().order_by('funcionario')

    if request.method == "POST":
        try:
            funcionario = get_object_or_404(Funcionario, pk=request.POST.get('funcionario'))
            data_inicial = request.POST.get('data_inicial')
            data_final = request.POST.get('data_final')
            periodo = request.POST.get('periodo')
            tipo = request.POST.get('tipo')

            falta = FrequenciaFuncionarios(
                funcionario=funcionario,
                data_inicial=data_inicial,
                data_final=data_final,
                periodo=periodo,
                tipo=tipo,
            )

            auditoria = Auditoria(
                acao=f'Falta de funcionário(a)',
                criado_por=user,
                info=f'Falta {tipo} para {funcionario}'
            )

            falta.save()
            auditoria.save()

            messages.success(request, 'Falta de funcionário(a) registrada com sucesso')
        
            return redirect('movimentacoes:faltas-funcionario')
        
        except Exception as e:
            print(f'Erro ao registrar falta de funcionário(a)')

            messages.error(request, 'Erro ao registrar falta de funcionário(a)')

            return redirect('movimentacoes:faltas-funcionario')

    context = {
        'funcionarios': funcionarios,
        'faltas': faltas,
        'tipos': TIPOS_FUNCIONARIOS,
        'periodos': PERIODOS
    }

    return render(request, 'faltas_funcionario.html', context)

@login_required
def excluir_faltas_funcionario(request, pk):
    user = request.user.get_full_name()
    falta = get_object_or_404(FrequenciaFuncionarios, pk=pk)

    if falta:
        try:
            auditoria = Auditoria(
                acao=f'Exclusão de falta de funcionário',
                criado_por=user,
                info=f'Falta de {falta.data_inicial} do {falta.funcionario} excluída'
            )
            auditoria.save()
            falta.delete()

            messages.success(request, 'Falta excluída com sucesso')

            return redirect('movimentacoes:faltas-funcionario')


        except Exception as e:
            print(f'Erro ao excluir falta de funcionário: {e}')

            messages.error(request, 'Erro ao excluir falta de funcionário(a), consulte o administrador')

    return redirect('movimentacoes:faltas-funcionario')

def comunicar_movimentacao(request):
    pk = request.GET.get('id')
    movimentacao = get_object_or_404(Movimentacoes, pk=pk)
    aluno = movimentacao.aluno
    nascimento = movimentacao.aluno.nascimento.strftime('%d/%m/%Y') if movimentacao.aluno.nascimento else 'Não definido' # type: ignore
    origem = movimentacao.origem if movimentacao.origem else movimentacao.origem_input
    destino = movimentacao.destino if movimentacao.destino else movimentacao.destino_input
    data = movimentacao.data.strftime("%d/%m/%Y") # type: ignore

    context = []

    context.append({'tipo': movimentacao.tipo},)
    context.append({'aluno': str(aluno)},)
    context.append({'nascimento': str(nascimento)},)
    context.append({'origem': str(origem)},)
    context.append({'destino': str(destino)},)
    context.append({'data': str(data)},)

    if movimentacao.origem:
        professores_origem = Sala.objects.get(pk=movimentacao.origem.pk)
        for atribuicao in professores_origem.atribuicoes.all(): # type: ignore
            context.append({
                'nome': atribuicao.professor.user.get_full_name(),
                'telefone': atribuicao.professor.telefone,
            })

    if movimentacao.destino:
        professores_destino = Sala.objects.get(pk=movimentacao.destino.pk)
        for atribuicao in professores_destino.atribuicoes.all(): # type: ignore
            context.append({
                'nome': atribuicao.professor.user.get_full_name(),
                'telefone': atribuicao.professor.telefone
            })

    return JsonResponse(context, safe=False)

def altera_numero_aluno(request, pk, numero):
    turma = Turma.objects.get(pk=pk)

    if turma:
        turma.numero_aluno = numero
        turma.save()

        return JsonResponse({"ok": "Número de aluno alterado com sucesso"})
    
