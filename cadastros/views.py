from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def salas(request):

    context = {}

    return render(request, 'salas.html', context)

@login_required
def disciplinas(request):

    context = {}

    return render(request, 'disciplinas.html', context)

@login_required
def professores(request):

    context = {}

    return render(request, 'professores.html', context)

@login_required
def alunos(request):

    context = {}

    return render(request, 'alunos.html', context)
