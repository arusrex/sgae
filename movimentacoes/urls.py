from django.urls import path
from movimentacoes import views

app_name = 'movimentacoes'

urlpatterns = [
    path('movimentacoes/', views.movimentacoes, name='movimentacoes'),

    path('turmas/', views.turmas, name='turmas'),

    path('atribuicao-professor/', views.atribuicao_professor, name='atribuicoes'),

    path('faltas-professor/', views.faltas_professor, name='faltas-professor'),
]
