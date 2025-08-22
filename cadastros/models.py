from django.db import models
from core.models import ControleDeRegistros
from usuarios.models import Usuarios
from datetime import date

ano_atual = date.today().year

class Sala(ControleDeRegistros):
    numero = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=10)
    ano = models.IntegerField(default=ano_atual)

    def __str__(self):
        return self.nome

class Disciplina(ControleDeRegistros):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

class Professor(ControleDeRegistros):
    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE, related_name='professor')
    matricula = models.CharField(max_length=30, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    funcao = models.CharField(max_length=150, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

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
