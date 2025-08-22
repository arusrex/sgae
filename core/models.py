from django.db import models

class ControleDeRegistros(models.Model):
    acao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.CharField(max_length=100, blank=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    atualizado_por = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    info = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
