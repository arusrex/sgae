from .models import Turma, AtribuicaoProfessor, Movimentacoes
from cadastros.models import Aluno, Sala
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def movimentacoes(request, pk=None):
    user = request.user.get_full_name()
    alunos = Aluno.objects.all().order_by('nome')
    salas = Sala.objects.filter(ano=datetime.date.today().year)

    context = {
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

    return render(request, 'turmas.html')