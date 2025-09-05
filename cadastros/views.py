from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from .models import Sala, Disciplina, Professor, Aluno
from usuarios.models import Usuarios
from core.models import Auditoria

@login_required
def salas(request, pk=None):
    user = request.user
    salas = Sala.objects.all()
    
    if pk:
        sala = get_object_or_404(Sala, pk=pk)
    else:
        sala = None

    if sala and request.method == 'POST':

        sala.numero = request.POST['numero']
        sala.nome = request.POST['nome']
        sala.ano = request.POST['ano']

        Auditoria.objects.create(
            acao="Edição de sala",
            atualizado_por=user.get_full_name(),
            info=f"{sala.nome} - {sala.ano} editada"
        )

        sala.save()

        return redirect('cadastros:salas')
    
    if not sala and request.method == 'POST':
        numero = request.POST['numero']
        nome = request.POST['nome']
        ano = request.POST['ano']

        sala = Sala.objects.create(
            numero=numero,
            nome=nome,
            ano=ano
        )

        Auditoria.objects.create(
            acao="Criação de sala",
            atualizado_por=user.get_full_name(),
            info=f"{sala.nome} - {sala.ano} criada"
        )

        return redirect('cadastros:salas')

    context = {
        'salas': salas,
        'sala': sala
    }

    return render(request, 'salas.html', context)

def excluir_sala(request, pk):
    user = request.user
    sala = get_object_or_404(Sala, pk=pk)

    if sala:
        Auditoria.objects.create(
            acao="Exclusão de sala",
            atualizado_por=user.get_full_name(),
            info=f"{sala.nome} - {sala.ano} excluída"
        )
        sala.delete()
    
    return redirect('cadastros:salas')

@login_required
def disciplinas(request, pk=None):
    user = request.user
    disciplinas = Disciplina.objects.all()

    if pk:
        disciplina = get_object_or_404(Disciplina, pk=pk)
    else:
        disciplina = None
    
    if disciplina is not None and request.method == 'POST':
        disciplina.nome = request.POST['nome']
        disciplina.atualizado_por = user.get_full_name()

        Auditoria.objects.create(
            acao='Edição de disciplina',
            atualizado_por=user.get_full_name(),
            info=f'{disciplina.nome} atualizada'
        )

        disciplina.save()

        return redirect('cadastros:disciplinas')

    elif disciplina == None and request.method == 'POST':
        nome = request.POST['nome']

        disciplina = Disciplina.objects.create(
            nome=nome,
            criado_por=user.get_full_name()
        )

        return redirect('cadastros:disciplinas')

    context = {
        'disciplinas': disciplinas,
        'disciplina': disciplina,
    }

    return render(request, 'disciplinas.html', context)

@login_required
def excluir_disciplina(request, pk):
    user = request.user
    disciplina = get_object_or_404(Disciplina, pk=pk)

    if disciplina:
        Auditoria.objects.create(
            acao='Exclusão de disciplina',
            criado_por=user.get_full_name(),
            info=f'{disciplina.nome} excluída'
        )
        disciplina.delete()

    return redirect('cadastros:salas')

@login_required
def professores(request, pk=None):
    user = request.user
    professores = Professor.objects.all()

    if pk:
        professor = get_object_or_404(Professor, pk=pk)
        usuario = professor.user

    else:
        professor = None
        usuario = None

    if request.method == 'POST':
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        senha1 = request.POST['senha']
        senha2 = request.POST['confirmar-senha']
        matricula = request.POST['matricula']
        cpf = request.POST['cpf']
        rg = request.POST['rg']
        nascimento = request.POST['nascimento']
        funcao = request.POST['funcao']
        telefone = request.POST['telefone']
        endereco = request.POST['endereco']
        observacoes = request.POST['observacoes']

        email_exists = Usuarios.objects.filter(email=email).exists()

        if professor is not None and usuario is not None:
            if usuario.email != email:
                email_diferente = Usuarios.objects.filter(email=email).exclude(pk=usuario.pk).exists()
                if email_diferente:
                    return redirect('cadastros:professores')
            
            usuario.first_name = nome
            usuario.last_name = sobrenome
            usuario.email = email

            if senha1 is not None and senha1 == senha2:
                usuario.set_password(senha1)

            usuario.cpf = cpf

            usuario.save()

            professor.matricula = matricula
            professor.rg = rg
            professor.nascimento = nascimento
            professor.funcao = funcao
            professor.telefone = telefone
            professor.endereco = endereco
            professor.observacoes = observacoes
            professor.atualizado_por = user.get_full_name()

            professor.save()
            
            return redirect('cadastros:professores')
        else:
            if senha1 == '' or senha1 != senha2 or email_exists:
                return redirect('cadastros:professores')
            
            usuario_criado = Usuarios(
                first_name=nome,
                last_name=sobrenome,
                email=email,
                cpf=cpf
            )
            usuario_criado.set_password(senha1)
            usuario_criado.save()

            if usuario_criado:
                professor_criado = Professor(
                    user=usuario_criado,
                    matricula=matricula,
                    rg=rg,
                    nascimento=nascimento,
                    funcao=funcao,
                    telefone=telefone,
                    endereco=endereco,
                    observacoes=observacoes,
                    criado_por=user.get_full_name()
                )
                professor_criado.save()

            return redirect('cadastros:professores')

    context = {
        'professores': professores,
        'professor': professor,
        'usuario': usuario
    }

    return render(request, 'professores.html', context)

@login_required
def excluir_professor(request, pk):
    user = request.user
    professor = get_object_or_404(Professor, pk=pk)

    if professor:
        auditoria = Auditoria(
            acao='Exclusão de professor(a)',
            criado_por=user.get_full_name(),
            info=f'Professor(a) {professor} excluído'
        )
        professor.delete()
        auditoria.save()
    
    return redirect('cadastros:professores')

@login_required
def alunos(request, pk=None):
    alunos = Aluno.objects.all()

    context = {
        'tansportes': Aluno.TRANSPORTE,
        'generos': Aluno.SEXO,
        'estados': Aluno.ESTADOS,
        'alunos': alunos
    }

    return render(request, 'alunos.html', context)

def excluir_aluno(request, pk):
    return redirect('cadastros:alunos')
