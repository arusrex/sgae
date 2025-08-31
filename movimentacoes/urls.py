from django.urls import path
from movimentacoes import views

app_name = 'movimentacoes'

urlpatterns = [
    path('matricula/', views.matriculas, name='matriculas'),
    path('remanejamento/', views.remanejamentos, name='remanejamentos'),
    path('transferencia/', views.transferencias, name='transferencias'),
]
