from django.db import models
from core.models import ControleDeRegistros
from cadastros.models import Professor

class Avisos(ControleDeRegistros):
    TIPOS = [
        ('matricula', 'Matrícula'),
        ('remanejamento', 'Remanejamento'),
        ('transferencia', 'Transferência'),
        ('outros', 'Outros')
    ]

    STATUS = [
        ('pendente', 'Pendente'),
        ('enviado', 'Enviado'),
        ('erro', 'Erro')
    ]

    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, blank=True, null=True)
    mensagem = models.TextField(blank=True, null=True)
    envio = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=30, choices=TIPOS, default='Matrícula')
    status = models.CharField(max_length=30, choices=STATUS, default='Pendente')

    def __str__(self):
        professor = self.professor.user.get_full_name() if self.professor else 'Sem professor'
        return f'Mensagem de {self.tipo} para {professor}'
