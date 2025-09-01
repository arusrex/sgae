from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def matriculas(request):

    context = {}

    return render(request, 'matriculas.html', context)

@login_required
def remanejamentos(request):

    context = {}

    return render(request, 'remanejamentos.html', context)

@login_required
def transferencias(request):

    context = {}

    return render(request, 'transferencias.html', context)
