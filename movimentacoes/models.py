from django.db import models
from cadastros.models import Professor, Aluno, Sala
from core.models import ControleDeRegistros
from datetime import date

ano_atual = date.today().year

class Turma(ControleDeRegistros):
    STATUS = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('remanejado', 'Remanejado'),
        ('transferido', 'Transferido'),
        ('concluido', 'Concluído'),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, blank=True, null=True, related_name='turmas')
    aluno = models.ForeignKey(Aluno, on_delete=models.SET_NULL, blank=True, null=True, related_name='turmas')
    numero_aluno = models.IntegerField(default=0)
    status = models.CharField(max_length=30, choices=STATUS, default='Ativo')

    def __str__(self):
        aluno = self.aluno.nome if self.aluno else "Sem aluno"
        sala = self.sala.nome if self.sala else "Sem sala"
        ano = self.sala.ano if self.sala else "Sem ano"

        return f"{aluno} - {sala} - {ano}"
    
class AtribuicaoProfessor(ControleDeRegistros):
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, blank=True, null=True)
    sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        professor = self.professor.user.get_full_name() if self.professor else "Sem professor(a)"
        sala = self.sala.nome if self .sala else "Sem sala"

        return f"Professor(a): {professor} - Sala: {sala}"
    
class Movimentacoes(ControleDeRegistros):
    TIPOS = [
        ('matricula', 'Matrícula'),
        ('remanejamento', 'Remanejamento'),
        ('transferencia', 'Transferência')
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.SET_NULL, blank=True, null=True)
    origem_input = models.CharField(max_length=150, blank=True, null=True)
    origem = models.ForeignKey(Sala, on_delete=models.SET_NULL, related_name='origem', blank=True, null=True)
    destino_input = models.CharField(max_length=150, blank=True, null=True)
    destino = models.ForeignKey(Sala, on_delete=models.SET_NULL, related_name='destino', blank=True, null=True)
    tipo = models.CharField(max_length=30, choices=TIPOS, default='Matrícula')
    data = models.DateField(blank=True, null=True)

    def __str__(self):
        aluno = self.aluno.nome if self.aluno else "Sem aluno"

        return f"{self.tipo} de {aluno}"
    
class FrequenciaProfessores(ControleDeRegistros):
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, blank=True, null=True)
    data_inicial = models.DateField(blank=True, null=True)
    data_final = models.DateField(blank=True, null=True)
    periodo = models.CharField(max_length=30, blank=True, null=True)
    quantidade = models.IntegerField(default=5)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        professor = self.professor.user.get_full_name() if self.professor else "Sem professor"

        return f"Professor(a): {professor}"
    

