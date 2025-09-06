from .models import Turma, AtribuicaoProfessor, Movimentacoes
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def movimentacoes(request, pk=None):
    user = request.user.get_full_name()

    context = {}

    return render(request, 'matriculas.html', context)

