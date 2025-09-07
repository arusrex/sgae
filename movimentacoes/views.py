from .models import Turma, AtribuicaoProfessor, Movimentacoes
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def movimentacoes(request, pk=None):
    user = request.user.get_full_name()

    context = {}

    return render(request, 'movimentacoes.html', context)

@login_required
def atribuicao_professor(request, pk=None):

    return render(request, 'atribuicao_professor.html')

@login_required
def faltas_professor(request, pk=None):

    return render(request, 'faltas_professor.html')