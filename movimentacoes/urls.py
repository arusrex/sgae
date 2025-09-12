from django.urls import path
from movimentacoes import views

app_name = 'movimentacoes'

urlpatterns = [
    path('movimentacoes/', views.movimentacoes, name='movimentacoes'),
    path('excluir-movimentacao/<str:pk>/', views.excluir_movimentacao, name='excluir-movimentacao'),
    path('matricula/', views.matricula, name='matricula'),

    path('turmas/', views.turmas, name='turmas'),
    path('excluir-turma/<str:pk>/', views.excluir_turma, name='excluir-turma'),

    path('atribuicao-professor/', views.atribuicao_professor, name='atribuicoes'),

    path('faltas-professor/', views.faltas_professor, name='faltas-professor'),
]
