from django.db import models
from core.models import ControleDeRegistros
from usuarios.models import Usuarios
from datetime import date

ano_atual = date.today().year

ESTADOS = [
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AP', 'AP'),
    ('AM', 'AM'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MT', 'MT'),
    ('MS', 'MS'),
    ('MG', 'MG'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PR', 'PR'),
    ('PE', 'PE'),
    ('PI', 'PI'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RS', 'RS'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('SC', 'SC'),
    ('SP', 'SP'),
    ('SE', 'SE'),
    ('TO', 'TO'),
]

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

    SEXO = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
    ]

    nome = models.CharField(max_length=150)
    rm = models.CharField(max_length=20, blank=True, null=True)
    ra = models.CharField(max_length=20, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=30, blank=True, null=True)
    nascimento = models.DateField(blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=2, choices=ESTADOS, blank=True, null=True)
    cor_raca = models.CharField(max_length=30, blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=SEXO, blank=True, null=True)
    necessita_educacao_especial = models.BooleanField(default=False)
    nis = models.CharField(max_length=80, blank=True, null=True)
    responsavel_1 = models.CharField(max_length=150, blank=True, null=True)
    contato_1 = models.CharField(max_length=30, blank=True, null=True)
    responsavel_2 = models.CharField(max_length=150, blank=True, null=True)
    contato_2 = models.CharField(max_length=30, blank=True, null=True)
    outros_contatos = models.CharField(max_length=255, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    medicamento = models.BooleanField(default=False)
    qual_medicamento = models.CharField(max_length=255, blank=True, null=True)
    diabete = models.BooleanField(default=False)
    alergia = models.BooleanField(default=False)
    cardiaco = models.BooleanField(default=False)
    mora_com_os_pais = models.BooleanField(default=True)
    motivo_mora_com_os_pais = models.CharField(max_length=255, blank=True, null=True)
    neuro = models.BooleanField(default=False)
    motivo_neuro = models.CharField(max_length=255, blank=True, null=True)
    psicologo = models.BooleanField(default=False)
    motivo_psicologo = models.CharField(max_length=255, blank=True, null=True)
    fono = models.BooleanField(default=False)
    motivo_fono = models.CharField(max_length=255, blank=True, null=True)
    integral = models.BooleanField(default=False)
    transporte = models.CharField(max_length=20, choices=TRANSPORTE, default='indefinido')
    obs_transporte = models.CharField(max_length=255, blank=True, null=True)
    retirada_aluno = models.CharField(max_length=255, blank=True, null=True)  
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
