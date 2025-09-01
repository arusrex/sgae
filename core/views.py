from django.shortcuts import render, redirect, get_list_or_404
from .models import Auditoria, Sistema

def login(request):

    context = {

    }

    return render(request, "login.html", context)

def registro(request):

    context = {}

    return render(request, "registro.html", context)

def redefinir_senha(request):

    context = {}

    return render(request, "redefinir_senha.html", context)

def index(request):
    auditoria = Auditoria.objects.all()

    if auditoria:
        context = {
            'auditoria': auditoria,
        }
    else:
        context = {}

    return render(request, 'index.html', context)

def sistema(request):
    dados = Sistema.objects.first()

    if not dados:
        nome = 'Sistema Administrativo',
        descricao = 'Administração e Gestão Descomplicada - ARUS DIGITAL TECH'
        logo = '/assets/img/arus_logo.png'
        cabecalho = '/assets/img/arus_logo.png'
        rodape = '/assets/img/arus_logo.png'

    context = {
        'nome': nome,
        'descricao': descricao,
        'logo': logo,
        'cabecalho': cabecalho,
        'rodape': rodape
    }

    return render(request, 'sistema.html', context)

def context_processors(request):
    dados = Sistema.objects.first()

    if not dados:
        nome = 'Sistema Administrativo'
        descricao = 'Administração e Gestão Descomplicada - ARUS DIGITAL TECH'
        logo = '/assets/img/arus_logo.png'
        cabecalho = '/assets/img/arus_logo.png'
        rodape = '/assets/img/arus_logo.png'

    context = {
        'sistema_nome': nome,
        'sistema_descricao': descricao,
        'sistema_logo': logo,
        'sistema_cabecalho': cabecalho,
        'sistema_rodape': rodape
    }

    return context