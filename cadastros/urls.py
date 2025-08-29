from django.urls import path
from cadastros import views

app_name = "cadastros"

urlpatterns = [
    path('salas/', views.salas, name='salas'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('professores/', views.professores, name='professores'),
    path('alunos/', views.alunos, name='alunos'),
]

