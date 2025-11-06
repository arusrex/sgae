from .models import Sistema
from movimentacoes.models import Movimentacoes, Turma
from cadastros.models import Sala
from django.db.models import Count
from datetime import datetime
from django.db.models import Q

def context_processors(request):
    dados = Sistema.objects.first()
    usuario = request.user

    if dados:
        nome = dados.nome
        descricao = dados.descricao if dados.descricao else 'Administração e Gestão - by ARUS DIGITAL TECH'
        logo = dados.logo if dados.logo else '/static/assets/img/arus_logo.png'
        redefinir_senha = dados.redefinir_senha
        nova_conta = dados.nova_conta
        logo_educacao = dados.logo_educacao if dados.logo_educacao else '/static/assets/img/arus_logo.png'
        logo_municipio = dados.logo_municipio if dados.logo_municipio else '/static/assets/img/arus_logo.png'
    else:
        nome = 'Sistema Administrativo Escolar'
        descricao = 'Administração e Gestão Descomplicada - by ARUS DIGITAL TECH'
        logo = '/static/assets/img/arus_logo.png'
        redefinir_senha =  False
        nova_conta = False
        logo_municipio = '/static/assets/img/arus_logo.png'
        logo_educacao = '/static/assets/img/arus_logo.png'

    context = {
        'usuario_sistema': usuario,
        'sistema_nome': nome,
        'sistema_descricao': descricao,
        'sistema_redefinir_senha': redefinir_senha,
        'sistema_nova_conta': nova_conta,
        'sistema_logo': logo,
        'sistema_logo_municipio': logo_municipio,
        'sistema_logo_educacao': logo_educacao
    }

    return context

ano_atual = datetime.now().year

def dados_graficos(request):
    alunos = Turma.objects.filter(status="Ativo")

    estatisticasAlunos = Turma.objects.values('status').annotate(total=Count('aluno')).filter(sala__ano=ano_atual)
    alunosAtivosPorSala = (
        Sala.objects.all()
        .filter(ano=ano_atual)
        .annotate(
            ativos=Count('turmas', Q(turmas__status='Ativo'))
            )
        ).order_by('serie', 'classe', 'periodo')
    
    context = {
        'graficos_alunos': estatisticasAlunos,
        'graficos_ativos_por_sala': alunosAtivosPorSala,
    }

    return context