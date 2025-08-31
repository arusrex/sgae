from django.shortcuts import render

def matriculas(request):

    context = {}

    return render(request, 'matriculas.html', context)

def remanejamentos(request):

    context = {}

    return render(request, 'remanejamentos.html', context)

def transferencias(request):

    context = {}

    return render(request, 'transferencias.html', context)
