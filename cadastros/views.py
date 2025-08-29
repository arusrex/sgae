from django.shortcuts import render

def salas(request):

    context = {}

    return render(request, 'salas.html', context)

def disciplinas(request):

    context = {}

    return render(request, 'disciplinas.html', context)

def professores(request):

    context = {}

    return render(request, 'professores.html', context)

def alunos(request):

    context = {}

    return render(request, 'alunos.html', context)
