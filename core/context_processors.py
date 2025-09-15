from .models import Sistema
from movimentacoes.models import Movimentacoes, Turma
from django.db.models import Count

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

def dados_graficos(request):
    alunos = Turma.objects.all()

    estatisticasAlunos = Turma.objects.values('status').annotate(total=Count('aluno'))

    context = {
        'graficos_alunos': estatisticasAlunos,
    }

    return context