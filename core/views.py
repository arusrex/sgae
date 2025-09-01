from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Auditoria, Sistema

def entrar(request):
    if request.method == 'POST':
        email = request.POST.get('inputEmail')
        senha = request.POST.get('inputPassword')

        usuario = authenticate(request, username=email, password=senha)

        if usuario:
            login(request, usuario)
            return redirect('index')
        else:
            print('Usuario ou senha inválido')

    return render(request, "login.html", {})

@login_required
def sair(request):
    logout(request)

    return redirect('core:login')

def registro(request):

    context = {}

    return render(request, "registro.html", context)

def redefinir_senha(request):

    context = {}

    return render(request, "redefinir_senha.html", context)

@login_required
def index(request):
    auditoria = Auditoria.objects.all()

    if auditoria:
        context = {
            'auditoria': auditoria,
        }
    else:
        context = {}

    return render(request, 'index.html', context)

@login_required
def sistema(request):
    dados = Sistema.objects.first()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        logo = request.FILES.get('logotipo')
        cabecalho = request.FILES.get('cabecalho')
        rodape = request.FILES.get('rodape')

        if dados:
            dados.nome = nome
            dados.descricao = descricao
            dados.logo = logo
            dados.cabecalho = cabecalho
            dados.rodape = rodape
        else:
            dados = Sistema.objects.create(
                nome=nome,
                descricao=descricao,
                logo=logo,
                cabecalho=cabecalho,
                rodape=rodape
            )
        
        Auditoria.objects.create(
            acao="Dados do sistema",
            info="Alteração nos dados do sistema"
        )

    return render(request, 'sistema.html')

def context_processors(request):
    dados = Sistema.objects.first()
    usuario = request.user

    if dados:
        nome = dados.nome
        descricao = dados.descricao if dados.descricao else 'Administração e Gestão - by ARUS DIGITAL TECH'
        logo = dados.logo if dados.logo else '/static/assets/img/arus_logo.png'
        cabecalho = dados.cabecalho if dados.cabecalho else '/static/assets/img/arus_logo.png'
        rodape = dados.rodape if dados.rodape else '/static/assets/img/arus_logo.png'
    else:
        nome = 'Sistema Administrativo'
        descricao = 'Administração e Gestão Descomplicada - by ARUS DIGITAL TECH'
        logo = '/static/assets/img/arus_logo.png'
        cabecalho = '/static/assets/img/arus_logo.png'
        rodape = '/static/assets/img/arus_logo.png'

    context = {
        'usuario': usuario,
        'sistema_nome': nome,
        'sistema_descricao': descricao,
        'sistema_logo': logo,
        'sistema_cabecalho': cabecalho,
        'sistema_rodape': rodape
    }

    return context