from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from core.models import Auditoria
from .models import Usuarios

@login_required
def usuarios(request):
    usuarios = Usuarios.objects.all()

    context = {
        'usuarios': usuarios,
    }

    return render(request, 'usuarios.html', context)

@login_required
def novo_usuario(request):
    user = request.user

    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        status = bool(request.POST.get('status'))
        senha1 = request.POST.get('senha')
        senha2 = request.POST.get('confirmar-senha')


        if senha1 != senha2:
            return render(request, 'form-usuario.html', {
            'nome': nome,
            'sobrenome': sobrenome,
            'email': email,
            'is_active': status,
            'erro': 'Senhas não coincidem!'
        })

        usuario = Usuarios.objects.create(
            first_name=nome,
            last_name=sobrenome,
            email=email,
            is_active=status,
            password=make_password(senha1)
        )

        Auditoria.objects.create(
            acao=f'Usúario criado',
            criado_por=user.get_full_name(),
            atualizado_por=user.get_full_name(),
            info=f"Novo usuário -  {usuario.get_full_name()}"
        )

        return redirect('usuarios:usuarios')

    return render(request, 'form-usuario.html')

@login_required
def editar_usuario(request, pk):
    user = request.user

    if request.method == 'POST':
        usuario = Usuarios.objects.get(pk=pk)
        usuario_id = usuario.pk

        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        status = bool(request.POST.get('status'))
        senha1 = request.POST.get('senha')
        senha2 = request.POST.get('confirmar-senha')

        email_existe = Usuarios.objects.filter(email=email).exclude(pk=usuario.pk).exists()

        if email_existe:
            return redirect('usuarios:editar-usuario', usuario.pk)
        else:
            usuario.first_name = nome
            usuario.last_name = sobrenome
            usuario.email = email
            usuario.is_active = status

            if senha1 and senha1 == senha2:
                usuario.password = make_password(senha1)
            
            usuario.save()

            Auditoria.objects.create(
                acao=f'Edição de usuário',
                atualizado_por=user.get_full_name(),
                info=f'O usuário foi editado - {usuario.get_full_name()}'
            )

            return redirect('usuarios:editar-usuario', usuario_id)
        
    usuario = Usuarios.objects.get(pk=pk)

    if usuario:
        
        context = {
                'nome': usuario.first_name,
                'sobrenome': usuario.last_name,
                'email': usuario.email,
                'is_active': usuario.is_active,
                'usuario_pk': usuario.pk
            }
        
        return render(request, 'form-usuario.html', context)
    
    else:

        return redirect('usuarios:usuarios')

@login_required
def status_usuario(request, pk):
    user = request.user
    usuario = Usuarios.objects.get(pk=pk)

    if usuario.is_active:
        usuario.is_active = False
        status = 'Ativo'
    else:
        usuario.is_active = True
        status = 'Inativo'
    
    usuario.save()

    Auditoria.objects.create(
        acao='Alteração de status de usuário',
        criado_por=user.get_full_name(),
        infor=f'Status atualizado para: {status}'
    )

    return redirect('usuarios:usuarios')
        
@login_required
def excluir_usuario(request, pk):
    user = request.user
    usuario = Usuarios.objects.get(pk=pk)

    if usuario:
        Auditoria.objects.create(
            acao=f'Exclusão de usuário',
            criado_por=user.get_full_name(),
            atualizado_por=user.get_full_name(),
            info=f'O usuário foi excluído - {usuario.get_full_name()}'
        )
        usuario.delete()
        return redirect('usuarios:usuarios')
    
    else:
        Auditoria.objects.create(
            acao=f'Erro na exclusão de usuário',
            criado_por=user.get_full_name(),
            atualizado_por=user.get_full_name(),
            info=f'Erro ao tentar excluir o usuário - {usuario.get_full_name()}'
        )
        return redirect('usuarios:usuarios')
