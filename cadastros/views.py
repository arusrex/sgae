from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Sala, Disciplina, Professor, Aluno
from 
from core.models import Auditoria

@login_required
def salas(request, pk=None):
    user = request.user
    salas = Sala.objects.all()
    
    if pk:
        sala = Sala.objects.get(pk=pk)
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
    sala = Sala.objects.get(pk=pk)

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
        disciplina = Disciplina.objects.get(pk=pk)
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
    disciplina = Disciplina.objects.get(pk=pk)

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
        professor = Professor.objects.get(pk=pk)
    else:
        professor = None
    
    if professor is not None and request.method == 'POST':


    context = {
        'professores': professores,
        'professor': professor
    }

    return render(request, 'professores.html', context)

@login_required
def excluir_professor(request):
    return redirect('cadastros:professores')

@login_required
def alunos(request):

    context = {}

    return render(request, 'alunos.html', context)
