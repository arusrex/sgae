from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.sistema, name='sistema'),
    path('login/', views.entrar, name="entrar"),
    path('logout/', views.sair, name='sair'),
    path('registro/', views.registro, name="registro"),
    path('redefinir_senha/', views.redefinir_senha, name="redefinir-senha"),
    path('dados_sistema_json/', views.dados_sistema_json, name="dados-sistema-json"),
]

