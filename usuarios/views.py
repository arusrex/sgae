from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from core.models import Auditoria
from .models import Usuarios
from django.contrib import messages

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
        try:
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

            usuario = Usuarios(
                first_name=nome,
                last_name=sobrenome,
                email=email,
                is_active=status,
            )
            usuario.set_password(senha1)
            usuario.save()

            Auditoria.objects.create(
                acao=f'Usúario criado',
                criado_por=user.get_full_name(),
                atualizado_por=user.get_full_name(),
                info=f"Novo usuário -  {usuario.get_full_name()}"
            )

            messages.success(request, 'Usuário cadastrado com sucesso')

            return redirect('usuarios:usuarios')
        
        except Exception as e:
            print(f'Erro ao cadastrar usuário: {e}')

            messages.error(request, 'Erro ao cadastrar usuário, consulte o administrador')

            return redirect('usuarios:usuarios')

    return render(request, 'form-usuario.html')

@login_required
def editar_usuario(request, pk):
    user = request.user

    if request.method == 'POST':
        try:
            usuario = Usuarios.objects.get(pk=pk)

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

                if senha1 and senha1 == senha2:
                    usuario.set_password(senha1)

                if user.pk == usuario.pk:
                    usuario.is_active = True
                else:
                    usuario.is_active = status
                            
                usuario.save()

                Auditoria.objects.create(
                    acao=f'Edição de usuário',
                    atualizado_por=user.get_full_name(),
                    info=f'O usuário foi editado - {usuario.get_full_name()}'
                )

                messages.success(request, 'Usuário editado com sucesso')

                return redirect('usuarios:editar-usuario', usuario.pk)
            
        except Exception as e:
            print(f'Erro ao editar usuário: {e}')

            messages.error(request, 'Erro ao editar usuário, consulte o administrador')

            return redirect('usuarios:editar-usuario', usuario.pk)
        
    usuario = Usuarios.objects.get(pk=pk)

    if usuario:
        
        context = {
                'nome': usuario.first_name,
                'sobrenome': usuario.last_name,
                'email': usuario.email,
                'is_active': usuario.is_active,
                'usuario': usuario
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
        info=f'Status atualizado para: {status}'
    )

    return redirect('usuarios:usuarios')
        
@login_required
def excluir_usuario(request, pk):
    user = request.user
    usuario = Usuarios.objects.get(pk=pk)

    if usuario:
        try:
            Auditoria.objects.create(
                acao=f'Exclusão de usuário',
                criado_por=user.get_full_name(),
                atualizado_por=user.get_full_name(),
                info=f'O usuário foi excluído - {usuario.get_full_name()}'
            )
            usuario.delete()

            messages.success(request, 'Usuário excluído com sucesso')

            return redirect('usuarios:usuarios')
        
        except Exception as e:
            print(f'Erro ao excluir usuario: {e}')

            messages.error(request, 'Erro ao excluir usuário')

    return redirect('usuarios:usuarios')


@login_required
def usuario_administrador(request, pk):
    usuario = Usuarios.objects.get(pk=pk)

    if usuario.is_superuser:
        usuario.is_superuser = False
        messages.warning(request, 'Usuário não é mais administrador')
    else:
        usuario.is_superuser = True
        messages.success(request, 'Usuário agora é administrador')
    
    usuario.save()

    return redirect('usuarios:usuarios')

@login_required
def atividades(request):
    user = request.user

    dados = Auditoria.objects.filter(
        Q(criado_por=user.get_full_name()) |
        Q(criado_por=user.email) |
        Q(atualizado_por=user.get_full_name()) |
        Q(atualizado_por=user.email)
        )

    context = {
        'dados': dados
    }

    return render(request, 'log_atividades.html', context)
