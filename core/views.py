from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import Auditoria, Sistema
from usuarios.models import Usuarios

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
        'usuario_sistema': usuario,
        'sistema_nome': nome,
        'sistema_descricao': descricao,
        'sistema_logo': logo,
        'sistema_cabecalho': cabecalho,
        'sistema_rodape': rodape
    }

    return context