from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from .models import Sala, Disciplina, Professor, Aluno
from usuarios.models import Usuarios
from core.models import Auditoria
from django.http import JsonResponse

@login_required
def salas(request, pk=None):
    user = request.user
    # salas = Sala.objects.filter(ano=date.today().year)
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

@login_required
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

    return redirect('cadastros:disciplinas')

@login_required
def professores(request, pk=None):
    user = request.user
    professores = Professor.objects.all()
    disciplinas = Disciplina.objects.all()

    if pk:
        professor = get_object_or_404(Professor, pk=pk)
        usuario = professor.user
        form_action = "form-editar-professor"
    else:
        professor = None
        usuario = None
        form_action = "form-cadastro-professor"

    if request.method == 'POST':
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        senha1 = request.POST['senha']
        senha2 = request.POST['confirmar-senha']
        matricula = request.POST['matricula']
        cpf = request.POST['cpf']
        rg = request.POST['rg']
        nascimento = request.POST.get('nascimento')
        funcao = request.POST['funcao']
        disciplina = get_object_or_404(Disciplina, pk=request.POST.get('disciplina')) or None
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
            professor.nascimento = nascimento if nascimento else None
            professor.funcao = funcao
            professor.disciplina = disciplina
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
                    nascimento=nascimento if nascimento else None,
                    funcao=funcao,
                    disciplina=disciplina,
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
        'usuario': usuario,
        'disciplinas': disciplinas,
        'form_action': form_action
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
def verificar_cpf_professor(request):
    cpf = request.GET.get('cpf')
    professor_existe = Professor.objects.filter(cpf=cpf).exists()
    return JsonResponse({"professor_existe": professor_existe})



@login_required
def alunos(request, pk=None):
    user = request.user
    alunos = Aluno.objects.all()


    if pk:
        aluno = get_object_or_404(Aluno, pk=pk)
        form_action = 'form-editar-aluno'
    else:
        form_action = 'form-cadastro-aluno'
        aluno = None
    
    if request.method == 'POST':
        nome = request.POST['nome']
        rm = request.POST['rm']
        ra = request.POST['ra']
        rg = request.POST['rg']
        cpf = request.POST['cpf']
        nascimento = request.POST['nascimento']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        cor_raca = request.POST['cor_raca']
        sexo = request.POST['sexo']
        nis = request.POST['nis']
        necessita_educacao_especial = bool(request.POST.get('necessita_educacao_especial'))
        diabete = bool(request.POST.get('diabete'))
        alergia = bool(request.POST.get('alergia'))
        cardiaco = bool(request.POST.get('cardiaco'))
        medicamento = bool(request.POST.get('medicamento'))
        qual_medicamento = request.POST['qual_medicamento']
        neuro = bool(request.POST.get('neuro'))
        motivo_neuro = request.POST['motivo_neuro']
        psicologo = bool(request.POST.get('psicologo'))
        motivo_psicologo = request.POST['motivo_psicologo']
        fono = bool(request.POST.get('fono'))
        motivo_fono = request.POST['motivo_fono']
        mora_com_os_pais = bool(request.POST.get('mora_com_os_pais'))
        motivo_mora_com_os_pais = request.POST['motivo_mora_com_os_pais']
        responsavel_1 = request.POST['responsavel_1']
        contato_1 = request.POST['contato_1']
        responsavel_2 = request.POST['responsavel_2']
        contato_2 = request.POST['contato_2']
        outros_contatos = request.POST['outros_contatos']
        endereco = request.POST['endereco']
        transporte = request.POST['transporte']
        obs_transporte = request.POST['obs_transporte']
        retirada_aluno = request.POST['retirada_aluno']
        integral = bool(request.POST.get('integral'))
        observacoes = request.POST.get('observacoes')

        if aluno is not None:

            aluno.nome = nome
            aluno.rm = rm
            aluno.ra = ra
            aluno.rg = rg
            aluno.cpf = cpf
            aluno.nascimento = nascimento if nascimento else None
            aluno.cidade = cidade
            aluno.estado = estado
            aluno.cor_raca = cor_raca
            aluno.sexo = sexo
            aluno.nis = nis
            aluno.necessita_educacao_especial = necessita_educacao_especial
            aluno.diabete = diabete
            aluno.alergia = alergia
            aluno.cardiaco = cardiaco
            aluno.medicamento = medicamento
            aluno.qual_medicamento = qual_medicamento
            aluno.neuro = neuro
            aluno.motivo_neuro = motivo_neuro
            aluno.psicologo = psicologo
            aluno.motivo_psicologo = motivo_psicologo
            aluno.fono = fono
            aluno.motivo_fono = motivo_fono
            aluno.mora_com_os_pais = mora_com_os_pais
            aluno.motivo_mora_com_os_pais = motivo_mora_com_os_pais
            aluno.responsavel_1 = responsavel_1
            aluno.contato_1 = contato_1
            aluno.responsavel_2 = responsavel_2
            aluno.contato_2 = contato_2
            aluno.outros_contatos = outros_contatos
            aluno.endereco = endereco
            aluno.transporte = transporte
            aluno.obs_transporte = obs_transporte
            aluno.retirada_aluno = retirada_aluno
            aluno.integral = integral
            aluno.atualizado_por = user.get_full_name()
            aluno.observacoes = observacoes

            aluno.save()

            return redirect('cadastros:alunos')
        
        else:

            aluno = Aluno(
            nome = nome,
            rm = rm,
            ra = ra,
            rg = rg,
            cpf = cpf,
            nascimento = nascimento if nascimento else None,
            cidade = cidade,
            estado = estado,
            cor_raca = cor_raca,
            sexo = sexo,
            nis = nis,
            necessita_educacao_especial = necessita_educacao_especial,
            diabete = diabete,
            alergia = alergia,
            cardiaco = cardiaco,
            medicamento = medicamento,
            qual_medicamento = qual_medicamento,
            neuro = neuro,
            motivo_neuro = motivo_neuro,
            psicologo = psicologo,
            motivo_psicologo = motivo_psicologo,
            fono = fono,
            motivo_fono = motivo_fono,
            mora_com_os_pais = mora_com_os_pais,
            motivo_mora_com_os_pais = motivo_mora_com_os_pais,
            responsavel_1 = responsavel_1,
            contato_1 = contato_1,
            responsavel_2 = responsavel_2,
            contato_2 = contato_2,
            outros_contatos = outros_contatos,
            endereco = endereco,
            transporte = transporte,
            obs_transporte = obs_transporte,
            retirada_aluno = retirada_aluno,
            integral = integral,
            criado_por = user.get_full_name(),
            observacoes = observacoes
            )

            aluno.save()

            return redirect('cadastros:alunos')

    context = {
        'transportes': Aluno.TRANSPORTE,
        'generos': Aluno.SEXO,
        'estados': Aluno.ESTADOS,
        'alunos': alunos,
        'aluno': aluno,
        'form_action': form_action
    }

    return render(request, 'alunos.html', context)

@login_required
def excluir_aluno(request, pk=None):
    user = request.user.get_full_name()
    if pk:
        aluno = get_object_or_404(Aluno, pk=pk)

        if aluno:
            auditoria = Auditoria(
                acao = "Exclusão de aluno",
                criado_por = user,
                info = f"Aluno(a) {aluno.nome} excluído"
            )
            auditoria.save()
            aluno.delete()

    return redirect('cadastros:alunos')

def ficha_aluno(request, pk=None):
    user = request.user.get_full_name()

    if pk:
        aluno = get_object_or_404(Aluno, pk=pk)

    context = {
        'aluno': aluno,
    }

    return render(request, 'ficha-aluno.html', context)


