from django.db import models
from datetime import date

ano_atual = date.today().year

class ControleDeRegistros(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.CharField(max_length=100, blank=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    atualizado_por = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True

class Sala(ControleDeRegistros):
    numero = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=10)

    def __str__(self):
        return self.nome

class Disciplina(ControleDeRegistros):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

class Professor(ControleDeRegistros):
    nome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=30, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=30, blank=True,  null=True)
    nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    funcao = models.CharField(max_length=150, blank=True, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Aluno(ControleDeRegistros):
    TRANSPORTE = [
        ('onibus', 'Onibus'),
        ('van', 'Van'),
        ('indefinido', 'Indefinido'),
    ]

    nome = models.CharField(max_length=150)
    rm = models.CharField(max_length=20, blank=True, null=True)
    ra = models.CharField(max_length=20, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=30, blank=True, null=True)
    nascimento = models.DateField(blank=True, null=True)
    nis = models.CharField(max_length=80, blank=True, null=True)
    responsavel_1 = models.CharField(max_length=150, blank=True, null=True)
    contato_1 = models.CharField(max_length=30, blank=True, null=True)
    responsavel_2 = models.CharField(max_length=150, blank=True, null=True)
    contato_2 = models.CharField(max_length=30, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    transporte = models.CharField(max_length=20, choices=TRANSPORTE, default='indefinido')
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Matricula(ControleDeRegistros):
    STATUS = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('tranferido', 'Transferido'),
        ('concluido', 'Concluído'),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, blank=True, null=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.SET_NULL, blank=True, null=True)
    ano = models.IntegerField(max_length=4, default=ano_atual)
    status = models.CharField(max_length=30, choices=STATUS, blank=True, null=True)

    def __str__(self):
        return f"{self.aluno.nome} - {self.sala.nome} - {self.ano}" # type: ignore
    
# class AtribuicaoProfessor(ControleDeRegistros):

