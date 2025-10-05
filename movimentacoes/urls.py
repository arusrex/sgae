from django.urls import path
from movimentacoes import views

app_name = 'movimentacoes'

urlpatterns = [
    path('movimentacoes/', views.movimentacoes, name='movimentacoes'),
    path('excluir-movimentacao/<str:pk>/', views.excluir_movimentacao, name='excluir-movimentacao'),
    path('matricula/', views.matricula, name='matricula'),
    path('remanejamento/', views.remanejamento, name='remanejamento'),
    path('transferencia/', views.transferencia, name='transferencia'),

    path('turmas/', views.turmas, name='turmas'),
    path('excluir-turma/<str:pk>/', views.turmas, name='excluir-turma'),
    path('turma/<str:pk>/', views.ficha_turma, name='ficha-turma'),
    path('excluir-turma/<str:pk>/', views.excluir_turma, name='excluir-turma'),

    path('atribuicao-professor/', views.atribuicao_professor, name='atribuicoes'),
    path('excluir-atribuicao-professor/<str:pk>/', views.excluir_atribuicoes, name='excluir-atribuicao'),

    path('faltas-professor/', views.faltas_professor, name='faltas-professor'),
    path('excluir-faltas-professor/<str:pk>/', views.excluir_faltas_professor, name='excluir-faltas-professor'),

    path('faltas-funcionario/', views.faltas_funcionario, name='faltas-funcionario'),
    path('excluir-faltas-funcionario/<str:pk>/', views.excluir_faltas_funcionario, name='excluir-faltas-funcionario'),
]
