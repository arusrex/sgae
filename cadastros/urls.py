from django.urls import path
from cadastros import views

app_name = "cadastros"

urlpatterns = [
    path('salas/', views.salas, name='salas'),
    path('editar-sala/<str:pk>/', views.salas, name='editar-sala'),
    path('excluir-sala/<str:pk>/', views.excluir_sala, name='excluir-sala'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('disciplinas/<str:pk>/', views.disciplinas, name='editar-disciplina'),
    path('excluir-discplina/<str:pk>/', views.excluir_disciplina, name='excluir-disciplina'),
    path('professores/', views.professores, name='professores'),
    path('editar-professor/<str:pk>/', views.professores, name='editar-professor'),
    path('excluir-professor/<str:pk>/', views.excluir_professor, name='excluir-professor'),
    path('alunos/', views.alunos, name='alunos'),
]

