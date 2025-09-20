import os
from core.models import Sistema
from .models import Aluno
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

def cabecalho_rodape(canvas, doc):
    dados = Sistema.objects.filter().first()

    # Estilos de texto
    styles = getSampleStyleSheet()
    titulo = styles["Title"]

    canvas.saveState()

    if dados and dados.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, dados.logo.name)  # se logo for ImageField
    else:
        logo_path = os.path.join(settings.BASE_DIR, "static", "assets", "img", "arus_logo.png")
    
    canvas.drawImage(logo_path, x=30, y=700, width=130, height=180)

    nome = dados.nome if dados else "Sistema Administrativo"
    canvas.setFont("Helvetica", 16)
    canvas.drawString(150, 800, nome)


    numero_pagina = canvas.getPageNumber()
    texto = f'Página {numero_pagina}'
    canvas.setFont("Helvetica", 8)
    canvas.drawString(500, 20, texto)

    texto_data = datetime.now().strftime("%d/%m/%Y %H:%M")
    canvas.drawString(40, 20, texto_data)

    canvas.restoreState()


def ficha_aluno(request, pk=None, tipo_pagina=None):
    sistema = Sistema.objects.first()
    aluno = get_object_or_404(Aluno, pk=pk)

    # Resposta como PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="relatorio.pdf"'

    # Documento base
    if tipo_pagina == None:
        tipo_pagina=A4

    doc = SimpleDocTemplate(
        response,
        pagesize=tipo_pagina,
        rightMargin=40,
        leftMargin=40,
        topMargin=100,
        bottonMargin=60
        )

    # Lista de elementos
    story = []

    # Estilos de texto
    styles = getSampleStyleSheet()
    titulo = styles["Title"]
    normal = styles["Normal"]
    bodytext = styles["BodyText"]

    # Adiciona título
    story.append(Paragraph("Ficha do Aluno", titulo))
    story.append(Spacer(1, 10))  # espaço entre blocos

    # Exemplo de tabela (boletim, contatos, etc.)
    dados = [
        [Paragraph(f"<b>Nome:</b> {aluno.nome} <b>R.M.:</b> {aluno.rm}  <b>R.A.:</b> {aluno.ra}", bodytext)],
        [Paragraph(f"<b>Nascimento:</b> {aluno.nascimento}", bodytext)],
        [Paragraph(f"<b>RA:</b> {aluno.ra}", bodytext)],
        [Paragraph(f"<b>Responsável:</b> {aluno.responsavel_1}", bodytext)],
    ]

    tabela = Table(dados, colWidths=500)
    tabela.setStyle(TableStyle([
        # ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        # ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    story.append(tabela)
    story.append(Spacer(1, 20))


    # Gera o PDF
    doc.build(story, onFirstPage=cabecalho_rodape, onLaterPages=cabecalho_rodape)
    return response

