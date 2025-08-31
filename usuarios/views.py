from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from core.models import Auditoria
from .models import Usuarios


def usuarios(request):
    usuarios = Usuarios.objects.all()

    context = {
        'usuarios': usuarios,
    }

    return render(request, 'usuarios.html', context)

def novo_usuario(request):

    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha1 = request.POST.get('senha')
        senha2 = request.POST.get('confirmar-senha')


        if senha1 != senha2:
            return render(request, 'form-usuario.html', {
            'nome': nome,
            'sobrenome': sobrenome,
            'email': email,
            'erro': 'Senhas não coincidem!'
        })

        usuario = Usuarios.objects.create(
            first_name=nome,
            last_name=sobrenome,
            email=email,
            password=make_password(senha1)
        )

        Auditoria.objects.create(
            acao=f'Usúario criado',
            info=f"Novo usuário -  {usuario.get_full_name()}"
        )

        return redirect('usuarios:usuarios')

    context = {}

    return render(request, 'form-usuario.html', context)

def editar_usuario(request, pk):

    if request.method == 'POST':
        usuario = Usuarios.objects.get(pk=pk)
        usuario_id = usuario.pk

        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha1 = request.POST.get('senha')
        senha2 = request.POST.get('confirmar-senha')

        email_existe = Usuarios.objects.filter(email=email).exclude(pk=usuario.pk).exists()

        if email_existe:
            return redirect('usuarios:editar-usuario', usuario.pk)
        else:
            usuario.first_name = nome
            usuario.last_name = sobrenome
            usuario.email = email

            if senha1 and senha1 == senha2:
                usuario.password = make_password(senha1)
            
            usuario.save()

            Auditoria.objects.create(
                acao=f'Edição de usuário',
                info=f'O usuário foi editado - {usuario.get_full_name()}'
            )

            return redirect('usuarios:editar-usuario', usuario_id)
        
    usuario = Usuarios.objects.get(pk=pk)

    if usuario:
        
        context = {
                'nome': usuario.first_name,
                'sobrenome': usuario.last_name,
                'email': usuario.email
            }
        
        return render(request, 'form-usuario.html', context)
    
    else:

        return redirect('usuarios:usuarios')
        

def excluir_usuario(request, pk):
    usuario = Usuarios.objects.get(pk=pk)

    if usuario:
        Auditoria.objects.create(
            acao=f'Exclusão de usuário',
            info=f'O usuário foi excluído - {usuario.get_full_name()}'
        )
        usuario.delete()
        return redirect('usuarios:usuarios')
    
    else:
        Auditoria.objects.create(
            acao=f'Erro na exclusão de usuário',
            info=f'Erro ao tentar excluir o usuário - {usuario.get_full_name()}'
        )
        return redirect('usuarios:usuarios')
