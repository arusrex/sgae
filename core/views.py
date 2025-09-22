from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import Auditoria, Sistema
from usuarios.models import Usuarios
from core.utils import redimensionar_imagem, tratar_imagens

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

    return redirect('core:entrar')

def registro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        senha1 = request.POST['senha']
        senha2 = request.POST['confirmar-senha']

        if senha1 == '' or senha1 != senha2:
            return render(request, 'registro.html', {
                'nome': nome,
                'sobrenome': sobrenome,
                'email':email
            })

        email_exists = Usuarios.objects.filter(email=email).exists()

        if email_exists:
            print('Email já registrado!')
            return render(request, 'registro.html', {
                'nome': nome,
                'sobrenome': sobrenome,
            })
        
        usuario = Usuarios.objects.create(
                first_name=nome,
                last_name=sobrenome,
                email=email,
                is_active=False,
                password=make_password(senha1)
            )
        
        Auditoria.objects.create(
            acao='Registro externo de usuário',
            criado_por=usuario.get_full_name(),
            info='Novo registro de usuário aguardando ativação no painel'
        )

        return redirect('core:entrar')

    return render(request, "registro.html")

def redefinir_senha(request):
    if request.method == 'POST':
        email = request.POST['email']

        if email == '':
            mensagem = 'Digite um e-mail!'
        
        if email:
            usuario = Usuarios.objects.filter(email=email).first()

            if usuario:
                mensagem = 'Um e-mail foi enviado com instruções para a redefinir sua senha!'
            else:
                mensagem = 'Usuário não encontrado'

        context = {
            'mensagem': mensagem,
        }
        return render(request, "redefinir_senha.html", context)
    

    return render(request, "redefinir_senha.html")

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
        logo_municipio = request.FILES.get('logo-municipio')
        logo_educacao = request.FILES.get('logo-educacao')

        logo_novo = tratar_imagens(logo, 85, 150, 150)
        logo_municipio_novo = tratar_imagens(logo_municipio, 85, 500, 500)
        logo_educacao_novo = tratar_imagens(logo_educacao, 85, 300, 300)

        if dados:
            dados.nome = nome
            dados.descricao = descricao

            if logo:
                dados.logo = logo_novo # type: ignore

            if logo_municipio:
                dados.logo_municipio = logo_municipio_novo # type: ignore

            if logo_educacao:
                dados.logo_educacao = logo_educacao_novo # type: ignore

            dados.save()

        else:
            dados = Sistema(
                nome=nome,
                descricao=descricao,
                logo=logo,
                logo_municipio=logo_municipio,
                logo_educacao=logo_educacao
            )

            dados.save()
        
        Auditoria.objects.create(
            acao="Dados do sistema",
            info="Alteração nos dados do sistema"
        )

        return redirect('core:sistema')

    return render(request, 'sistema.html')
