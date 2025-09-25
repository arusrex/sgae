from django.urls import path
from cadastros import views
from cadastros import report

app_name = "cadastros"

urlpatterns = [
    #SALAS
    path('salas/', views.salas, name='salas'),
    path('editar-sala/<str:pk>/', views.salas, name='editar-sala'),
    path('excluir-sala/<str:pk>/', views.excluir_sala, name='excluir-sala'),

    #DISCIPLINAS
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('disciplinas/<str:pk>/', views.disciplinas, name='editar-disciplina'),
    path('excluir-discplina/<str:pk>/', views.excluir_disciplina, name='excluir-disciplina'),

    #PROFESSORES
    path('professores/', views.professores, name='professores'),
    path('editar-professor/<str:pk>/', views.professores, name='editar-professor'),
    path('excluir-professor/<str:pk>/', views.excluir_professor, name='excluir-professor'),

    #ALUNOS
    path('alunos/', views.alunos, name='alunos'),
    path('editar-aluno/<str:pk>/', views.alunos, name='editar-aluno'),
    path('excluir-aluno/<str:pk>/', views.excluir_aluno, name='excluir-aluno'),
    path('ficha-do-aluno/<str:pk>/', views.ficha_aluno, name='ficha-aluno'),
    path('imprimir/ficha-do-aluno/<str:pk>/', report.ficha_aluno, name='imprimir-ficha-aluno'),
    path('verificar-cpf-professor/', views.verificar_cpf_professor, name='verificar-cpf-professor'),
]

