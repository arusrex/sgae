from django.db import models

class ControleDeRegistros(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.CharField(max_length=100, blank=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    atualizado_por = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True

class Sistema(ControleDeRegistros):
    nome = models.CharField(max_length=150, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='imagens/', blank=True, null=True)
    cabecalho = models.ImageField(upload_to='imagens/', blank=True, null=True)
    rodape = models.ImageField(upload_to='imagens/', blank=True, null=True)

    def __str__(self):
        return self.nome if self.nome else "Sistema Administrativo"
    
class Auditoria(ControleDeRegistros):
    acao = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.acao
