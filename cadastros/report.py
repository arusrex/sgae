import os
from core.models import Sistema
from usuarios.models import Usuarios
from .models import Aluno
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
from reportlab.pdfgen import canvas

def cabecalho_rodape(canvas, doc):
    dados = Sistema.objects.filter().first()
    user = usuario_sistema if usuario_sistema else ''

    x = 10
    y = 800

    # Estilos de texto
    styles = getSampleStyleSheet()
    titulo = styles["Title"]

    canvas.saveState()

    if dados and dados.logo:
        logo_path = os.path.join(settings.MEDIA_ROOT, dados.logo.name)  # se logo for ImageField
    else:
        logo_path = os.path.join(settings.BASE_DIR, "static", "assets", "img", "arus_logo.png")

    x += 30
    canvas.drawImage(logo_path, x, y-40, width=60, height=60)

    x += 75
    canvas.setFont("Times-Bold", 16)
    canvas.drawString(x, y, dados.nome if dados else "Sistema Administrativo")
    y -= 15
    canvas.setFont("Times-Roman", 14)
    canvas.drawString(x, y, "Secretaria de Educação")
    y -= 15
    canvas.setFont("Times-Roman", 12)
    canvas.drawString(x, y, "Prefeitura do Município de Jaú")


    numero_pagina = canvas.getPageNumber()
    texto = f'Página {numero_pagina}'
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(500, 20, texto)

    texto_data = datetime.now().strftime(f"%d/%m/%Y %H:%M Usuário: {usuario_sistema}")
    canvas.drawString(40, 20, texto_data)

    canvas.restoreState()


def ficha_aluno(request, pk=None, tipo_pagina=None):
    global usuario_sistema
    usuario_sistema = request.user

    estilo_titulo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ])

    estilo_simples = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.1, colors.black),
    ])

    sistema = Sistema.objects.first()
    aluno = get_object_or_404(Aluno, pk=pk)

    # Resposta como PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="ficha_aluno_{aluno.nome.replace(' ', '_')}.pdf"'

    # Documento base
    if tipo_pagina == None:
        tipo_pagina=A4

    doc = SimpleDocTemplate(
        response, # type: ignore
        pagesize=tipo_pagina,
        rightMargin=40,
        leftMargin=40,
        topMargin=100,
        bottonMargin=60
        )
    
    doc.title = f'ficha_aluno_{aluno.nome.replace(' ', '_')}'
    doc.author = "Secretaria da Escola"
    doc.subject = "Relatório Individual"
    doc.keywords = ["Aluno", "Ficha", "Escola"]

    # Lista de elementos
    story = []

    # Estilos de texto
    styles = getSampleStyleSheet()
    titulo = styles["Title"]
    sub_titulo = styles["Heading1"]
    normal = styles["Normal"]
    bodytext = styles["BodyText"]

    # Adiciona título
    story.append(Paragraph("Ficha do Aluno", titulo))
    story.append(Spacer(1, 10))  # espaço entre blocos
    story.append(Paragraph("Dados pessoais", sub_titulo))
    story.append(Spacer(1, 10))  # espaço entre blocos

    # Exemplo de tabela (boletim, contatos, etc.)

    p1 = [[
        Paragraph(f"<b>Nome:</b> {aluno.nome}", bodytext),
        Paragraph(f"<b>R.M.:</b> {aluno.rm}", bodytext),
        Paragraph(f"<b>R.A.:</b> {aluno.ra}", bodytext)
    ]]

    p2 = [[
        Paragraph(f"<b>R.G.:</b> {aluno.rg}", bodytext),
        Paragraph(f"<b>C.P.F.:</b> {aluno.cpf}", bodytext),
        Paragraph(f"<b>N.I.S.:</b> {aluno.nis}", bodytext),
        Paragraph(f"<b>Nasc.:</b> {aluno.nascimento}", bodytext)
    ]]

    p3 = [[
        Paragraph(f"<b>Cidade:</b> {aluno.cidade}", bodytext),
        Paragraph(f"<b>Estado:</b> {aluno.estado}", bodytext),
        Paragraph(f"<b>Gênero:</b> {aluno.sexo}", bodytext),
        Paragraph(f"<b>Raça/Etnia:</b> {aluno.cor_raca}", bodytext)
    ]]

    p4 = [[
        Paragraph(f"<b>Endereço:</b> {aluno.endereco}", bodytext),
    ]]

    p5 = [[
        Paragraph(f"<b>Filiação 1:</b> {aluno.responsavel_1}", bodytext),
        Paragraph(f"<b>Contato:</b> {aluno.contato_1}", bodytext),
    ]]

    p6 = [[
        Paragraph(f"<b>Filiação 1:</b> {aluno.responsavel_2}", bodytext),
        Paragraph(f"<b>Contato:</b> {aluno.contato_2}", bodytext),
    ]]

    p7 = [[
        Paragraph(f"<b>Outros contatos:</b> {aluno.outros_contatos}", bodytext),
    ]]
    moraComOsPais = "Sim" if aluno.mora_com_os_pais else "Não"
    p8 = [[
        Paragraph(f"<b>Mora com os pais?:</b> {moraComOsPais}", bodytext),
        Paragraph(f"<b>Motivo:</b> {aluno.motivo_mora_com_os_pais}", bodytext),
    ]]

    p9 = [[
        Paragraph(f"<b>Autorizados a retirar:</b> {aluno.retirada_aluno}", bodytext),
    ]]

    t1 = Table(p1, colWidths=[300,100,100])
    t1.setStyle(estilo_simples)
    t2 = Table(p2, colWidths=[125,125,125,125])
    t2.setStyle(estilo_simples)
    t3 = Table(p3, colWidths=[125,125,125,125])
    t3.setStyle(estilo_simples)
    t4 = Table(p4, colWidths=[500])
    t4.setStyle(estilo_simples)
    t5 = Table(p5, colWidths=[300,200])
    t5.setStyle(estilo_simples)
    t6 = Table(p6, colWidths=[300,200])
    t6.setStyle(estilo_simples)
    t7 = Table(p7, colWidths=[500])
    t7.setStyle(estilo_simples)
    t8 = Table(p8, colWidths=[150,350])
    t8.setStyle(estilo_simples)
    t9 = Table(p9, colWidths=[500])
    t9.setStyle(estilo_simples)

    story.append(t1)
    story.append(t2)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Localização/Contato", sub_titulo))
    story.append(Spacer(1, 10))
    story.append(t3)
    story.append(t4)
    story.append(t5)
    story.append(t6)
    story.append(t7)
    story.append(t8)
    story.append(t9)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Informações gerais", sub_titulo))
    story.append(Spacer(1, 10))
    story.append(t3)
    story.append(t4)
    story.append(t5)
    story.append(t6)
    story.append(t7)
    story.append(t8)
    story.append(t9)
    story.append(t8)
    story.append(t9)

    # Gera o PDF
    doc.build(story, onFirstPage=cabecalho_rodape, onLaterPages=cabecalho_rodape)
    return response

