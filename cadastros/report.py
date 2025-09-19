from .models import Aluno
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def ficha_aluno(request, pk=None):
    # Resposta como PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="relatorio.pdf"'

    # Documento base
    doc = SimpleDocTemplate(response, pagesize=A4)

    # Lista de elementos
    story = []

    # Estilos de texto
    styles = getSampleStyleSheet()
    titulo = styles["Title"]
    normal = styles["Normal"]

    # Adiciona título
    story.append(Paragraph("Ficha do Aluno", titulo))
    story.append(Spacer(1, 20))  # espaço entre blocos

    # Exemplo de dados do aluno
    aluno = {
        "nome": "João da Silva",
        "nascimento": "12/05/2015",
        "RA": "123456",
        "responsável": "Maria da Silva",
    }

    # Cria parágrafos
    story.append(Paragraph(f"<b>Nome:</b> {aluno['nome']} - <b>Nome:</b> {aluno['nome']}", normal))
    story.append(Paragraph(f"<b>Nascimento:</b> {aluno['nascimento']}", normal))
    story.append(Paragraph(f"<b>RA:</b> {aluno['RA']}", normal))
    story.append(Paragraph(f"<b>Responsável:</b> {aluno['responsável']}", normal))
    story.append(Spacer(1, 20))

    # Exemplo de tabela (boletim, contatos, etc.)
    dados = [
        ["Disciplina", "Nota"],
        ["Português", "8,5"],
        ["Matemática", "9,0"],
        ["História", "7,8"],
    ]

    tabela = Table(dados, colWidths=[200, 100])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))
    story.append(tabela)

    # Gera o PDF
    doc.build(story)
    return response

